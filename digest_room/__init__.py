"""Digest Room scaffold — NON-Switch logic only.

This package contains no Switch setup, no room creation, no agent connection,
and no Switch workflow. Those are built during the hackathon window (Nov 4-7)
per the official rule; building them on Nov 3 would break that rule.
What lives here is the portable logic the room will use once it exists:
the morning-digest text, the react-to-claim state machine, task cards,
the end-of-day summary, and the due-within-48h ping selector.

Python standard library only. All datetimes must be timezone-aware.
"""

from digest_room.digest import Opportunity, format_digest
from digest_room.claims import ClaimResult, ClaimStore, TaskCard

__all__ = [
    "Opportunity",
    "format_digest",
    "ClaimResult",
    "ClaimStore",
    "TaskCard",
]
