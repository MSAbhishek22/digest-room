"""Morning-digest formatting for the Digest Room.

Design voice (from DESIGN_CONSTITUTION.md): calm, precise, operator-like.
Every agent message carries the "Digest Room agent" source label and a
timestamp. Copy is short and factual; the agent prepares, humans decide —
the agent never registers, submits, or pays for anything.

This module only formats text. It does not post anywhere, does not connect
to Switch, and does not create a room.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


AGENT_LABEL = "Digest Room agent"


@dataclass(frozen=True)
class Opportunity:
    """One opportunity that may appear in the morning digest.

    ``deadline`` must be timezone-aware; naive datetimes are rejected so a
    deadline can never silently mean two different moments in two zones.
    """

    id: str
    title: str
    deadline: datetime
    prize: str
    fit_note: str

    def __post_init__(self) -> None:
        if not self.id:
            raise ValueError("opportunity id must not be empty")
        if not self.title:
            raise ValueError("opportunity title must not be empty")
        if self.deadline.tzinfo is None:
            raise ValueError("opportunity deadline must be timezone-aware")

    def is_expired_at(self, now: datetime) -> bool:
        return self.deadline < now


def _open_opportunities(
    opportunities: list[Opportunity], now: datetime
) -> list[Opportunity]:
    """Actionable opportunities only, earliest deadline first.

    An opportunity whose deadline is exactly ``now`` is still actionable
    (deadline >= now); anything earlier is expired and left out of the
    digest instead of being posted as if it could still be claimed.
    """
    open_ops = [o for o in opportunities if not o.is_expired_at(now)]
    open_ops.sort(key=lambda o: (o.deadline, o.id))
    return open_ops


def format_digest(opportunities: list[Opportunity], now: datetime) -> str:
    """Render the exact morning-digest message text the agent would post.

    Empty input (or everything expired) yields the empty-digest message,
    never a numbered list with no items and never a fake opportunity.
    """
    date_label = now.strftime("%Y-%m-%d")
    header = f"{AGENT_LABEL} — Morning digest — {date_label}"
    open_ops = _open_opportunities(opportunities, now)
    if not open_ops:
        return f"{header}\nNo new opportunities in today's digest."
    lines = [
        header,
        "React ✅ on an item to claim it. The agent prepares; humans register, "
        "submit, and pay — never the agent.",
        "",
    ]
    for index, opp in enumerate(open_ops, start=1):
        lines.append(f"{index}. {opp.title}")
        lines.append(
            f"   Deadline: {opp.deadline.isoformat()} | Prize: {opp.prize}"
        )
        lines.append(f"   Fit: {opp.fit_note}")
    lines.append("")
    lines.append(f"{len(open_ops)} opportunit{'y' if len(open_ops) == 1 else 'ies'} open.")
    return "\n".join(lines)
