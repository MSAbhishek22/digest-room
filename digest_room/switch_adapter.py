"""Switch / Mattermost adapter for the Digest Room — built 2026-11-04,
inside the Nov 4-7 hackathon window.

What this is, honestly:
- A translation layer between a chat-room event and the already-tested
  claim logic in claims.py. It does NOT fake a Switch room, does NOT
  claim a Switch connection exists, and does NOT post anywhere by itself.
- The real Switch room (Switch Console + Docker + bundled Mattermost,
  per the official quickstart) is the user's laptop step. When that room
  runs, this adapter is the exact point where a reaction event from
  that room enters the claim machine, and where the agent's reply text
  leaves it.

Event shape (what a real room sends, normalised here):
    {
      "type": "reaction_added",
      "user_id": "abhi",
      "message_id": "<digest item id>",   # = opportunity id in this build
      "emoji": "✅",
    }

Only "reaction_added" + "✅" is a claim. Anything else returns
{"handled": False} and changes nothing — a ❤️, a message edit, or a
bot's own reaction must never create a task card.

The agent's room instructions live in switch/ROOM_INSTRUCTIONS.md.
The laptop setup steps live in switch/SWITCH_SETUP.md.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from digest_room.claims import ClaimStore, format_claim_confirmation


@dataclass(frozen=True)
class RoomEventResult:
    handled: bool
    reply_text: str | None
    claim_status: str | None


def handle_room_event(
    store: ClaimStore, event: dict, now: datetime
) -> RoomEventResult:
    """Translate one room event into a claim (or a deliberate no-op)."""
    if not isinstance(event, dict):
        return RoomEventResult(False, None, None)
    if event.get("type") != "reaction_added":
        return RoomEventResult(False, None, None)
    if event.get("emoji") != "✅":
        return RoomEventResult(False, None, None)
    user_id = event.get("user_id")
    message_id = event.get("message_id")
    if not user_id or not message_id:
        return RoomEventResult(False, None, None)
    result = store.claim(str(user_id), str(message_id), now)
    reply = format_claim_confirmation(result, now)
    return RoomEventResult(True, reply, result.status)


def digest_post_text(digest_text: str) -> str:
    """The exact text the agent posts into the room for a digest.

    Kept as a pass-through on purpose: formatting is owned and tested
    in digest.py, so the adapter cannot silently reword a digest.
    """
    return digest_text
