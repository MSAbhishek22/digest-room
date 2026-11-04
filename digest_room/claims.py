"""React-to-claim state machine for the Digest Room.

Rules, taken from DESIGN_CONSTITUTION.md and the build pack:
- One click on ✅ claims an opportunity for one user and creates one task
  card. The card is what appears in the claimed-tasks rail.
- Idempotency: the same user claiming the same opportunity twice gets the
  existing card back with "already claimed by you" — never a second card.
  A different user claiming the same opportunity gets their own card.
- An expired opportunity cannot be claimed; an unknown id cannot be claimed.
- The agent never registers, submits, or pays; a task card is preparation
  only, and the human owner still has to do the tapping.
- The end-of-day summary reports claimed / still open / expired-unclaimed.
- The due-within-48h ping selector returns claimed tasks whose deadline
  falls in [now, now + 48h], earliest first — the owners the agent pings.

This module holds state in memory only. It does not talk to Switch, does
not create a room, and does not send any message anywhere.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta

from digest_room.digest import AGENT_LABEL, Opportunity

PING_WINDOW = timedelta(hours=48)


@dataclass(frozen=True)
class TaskCard:
    """One claimed task, as it would appear in the claimed-tasks rail."""

    id: str
    opportunity_id: str
    owner: str
    title: str
    deadline: datetime
    claimed_at: datetime


@dataclass(frozen=True)
class ClaimResult:
    """Outcome of one claim attempt. Exactly one status is set."""

    status: str  # "claimed" | "already_claimed" | "expired" | "unknown"
    card: TaskCard | None
    message: str


def format_claim_confirmation(result: ClaimResult, now: datetime) -> str:
    """Render the agent's in-thread confirmation text for a claim result."""
    stamp = now.strftime("%Y-%m-%d %H:%M")
    if result.card is None:
        return f"{AGENT_LABEL} — {stamp} — {result.message}"
    if result.status == "already_claimed":
        return (
            f"{AGENT_LABEL} — {stamp} — already claimed by you: "
            f"{result.card.title} (due {result.card.deadline.isoformat()}). "
            "Your existing task card is unchanged."
        )
    return (
        f"{AGENT_LABEL} — {stamp} — ✅ Claimed by {result.card.owner}: "
        f"{result.card.title} (due {result.card.deadline.isoformat()}). "
        "Task card created."
    )


class ClaimStore:
    """In-memory claim state for one digest day's opportunities."""

    def __init__(self, opportunities: list[Opportunity]) -> None:
        self._opportunities: dict[str, Opportunity] = {}
        for opp in opportunities:
            if opp.id in self._opportunities:
                raise ValueError(f"duplicate opportunity id: {opp.id!r}")
            self._opportunities[opp.id] = opp
        self._claims: dict[tuple[str, str], TaskCard] = {}
        self._cards_in_order: list[TaskCard] = []

    def claim(
        self, user_id: str, opportunity_id: str, now: datetime
    ) -> ClaimResult:
        opp = self._opportunities.get(opportunity_id)
        if opp is None:
            return ClaimResult(
                status="unknown",
                card=None,
                message=f"Unknown opportunity: {opportunity_id!r}. Nothing claimed.",
            )
        if opp.is_expired_at(now):
            return ClaimResult(
                status="expired",
                card=None,
                message=(
                    f"{opp.title!r} is past its deadline "
                    f"({opp.deadline.isoformat()}). Nothing claimed."
                ),
            )
        key = (user_id, opportunity_id)
        existing = self._claims.get(key)
        if existing is not None:
            return ClaimResult(
                status="already_claimed",
                card=existing,
                message="already claimed by you",
            )
        card = TaskCard(
            id=f"T-{opportunity_id}-{user_id}",
            opportunity_id=opportunity_id,
            owner=user_id,
            title=opp.title,
            deadline=opp.deadline,
            claimed_at=now,
        )
        self._claims[key] = card
        self._cards_in_order.append(card)
        return ClaimResult(status="claimed", card=card, message="claimed")

    def task_cards(self) -> list[TaskCard]:
        return list(self._cards_in_order)

    def end_of_day_summary(self, now: datetime) -> str:
        """Claimed / still open / expired-unclaimed, for the end-of-day post."""
        date_label = now.strftime("%Y-%m-%d")
        header = f"{AGENT_LABEL} — End-of-day summary — {date_label}"
        claimed_ids = {c.opportunity_id for c in self._cards_in_order}
        open_ops = [
            o
            for o in self._opportunities.values()
            if o.id not in claimed_ids and not o.is_expired_at(now)
        ]
        expired_ops = [
            o
            for o in self._opportunities.values()
            if o.id not in claimed_ids and o.is_expired_at(now)
        ]
        open_ops.sort(key=lambda o: (o.deadline, o.id))
        expired_ops.sort(key=lambda o: (o.deadline, o.id))
        if not self._cards_in_order and not open_ops and not expired_ops:
            return f"{header}\nNothing to report today."
        lines = [header, ""]
        lines.append("Claimed:")
        if self._cards_in_order:
            for card in self._cards_in_order:
                lines.append(
                    f"  ✅ {card.title} — {card.owner} "
                    f"(due {card.deadline.isoformat()})"
                )
        else:
            lines.append(
                "  No claims yet today — react ✅ on a digest item to claim it."
            )
        lines.append("")
        lines.append("Still open:")
        if open_ops:
            for opp in open_ops:
                lines.append(
                    f"  ○ {opp.title} (due {opp.deadline.isoformat()})"
                )
        else:
            lines.append("  Nothing still open.")
        lines.append("")
        lines.append("Expired unclaimed:")
        if expired_ops:
            for opp in expired_ops:
                lines.append(
                    f"  ✕ {opp.title} (was due {opp.deadline.isoformat()})"
                )
        else:
            lines.append("  None.")
        return "\n".join(lines)

    def due_within_48h(self, now: datetime) -> list[TaskCard]:
        """Claimed tasks due in [now, now + 48h], earliest deadline first.

        These are the owners the agent pings. Unclaimed opportunities have
        no owner, so they are never in this list; expired tasks are not
        "due soon", they are overdue, so they are excluded too.
        """
        window_end = now + PING_WINDOW
        due = [
            card
            for card in self._cards_in_order
            if now <= card.deadline <= window_end
        ]
        due.sort(key=lambda c: (c.deadline, c.id))
        return due
