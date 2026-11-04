"""Unit tests for the Digest Room scaffold (stdlib unittest only).

These tests cover the portable logic only: digest formatting, the claim
state machine, the end-of-day summary, and the 48h ping selector. They do
not touch Switch, any network, or any room — there is nothing to connect
to, by design, until the Nov 4-7 build window.

Run from the project root:
    python3 -m unittest discover -s tests -t . -v
"""

import unittest
from datetime import datetime, timedelta, timezone

from digest_room.claims import ClaimStore, format_claim_confirmation
from digest_room.digest import Opportunity, format_digest

UTC = timezone.utc
NOW = datetime(2026, 11, 4, 7, 0, tzinfo=UTC)


def opp(opp_id, title, deadline, prize="$1,000", fit="fits"):
    return Opportunity(
        id=opp_id, title=title, deadline=deadline, prize=prize, fit_note=fit
    )


class TestDigestFormatting(unittest.TestCase):
    def test_lists_items_sorted_by_deadline_with_all_fields(self):
        opps = [
            opp("b", "Beta", NOW + timedelta(days=5), "$5,000", "agent fit"),
            opp("a", "Alpha", NOW + timedelta(days=2), "$2,000", "strong fit"),
        ]
        text = format_digest(opps, NOW)
        self.assertIn("Digest Room agent", text)
        self.assertIn("2026-11-04", text)
        self.assertLess(text.index("Alpha"), text.index("Beta"))
        self.assertIn("Alpha", text)
        self.assertIn("$2,000", text)
        self.assertIn("strong fit", text)
        self.assertIn("2 opportunities open.", text)

    def test_empty_digest_has_no_items(self):
        text = format_digest([], NOW)
        self.assertIn("No new opportunities in today's digest.", text)
        self.assertNotIn("1.", text)

    def test_expired_opportunities_excluded(self):
        opps = [
            opp("old", "Gone", NOW - timedelta(hours=1)),
            opp("live", "Live", NOW + timedelta(days=1)),
        ]
        text = format_digest(opps, NOW)
        self.assertNotIn("Gone", text)
        self.assertIn("Live", text)
        self.assertIn("1 opportunity open.", text)

    def test_deadline_exactly_now_is_still_actionable(self):
        text = format_digest([opp("edge", "Edge", NOW)], NOW)
        self.assertIn("Edge", text)

    def test_all_expired_yields_empty_digest(self):
        text = format_digest([opp("old", "Gone", NOW - timedelta(days=1))], NOW)
        self.assertIn("No new opportunities in today's digest.", text)

    def test_opportunity_validation(self):
        with self.assertRaises(ValueError):
            Opportunity(id="", title="X", deadline=NOW, prize="$1", fit_note="f")
        with self.assertRaises(ValueError):
            Opportunity(
                id="x",
                title="X",
                deadline=datetime(2026, 11, 4, 7, 0),  # naive: rejected
                prize="$1",
                fit_note="f",
            )


class TestClaimStateMachine(unittest.TestCase):
    def setUp(self):
        self.store = ClaimStore(
            [
                opp("a", "Alpha", NOW + timedelta(days=2)),
                opp("b", "Beta", NOW + timedelta(days=5)),
            ]
        )

    def test_claim_creates_one_task_card(self):
        result = self.store.claim("u1", "a", NOW)
        self.assertEqual(result.status, "claimed")
        self.assertIsNotNone(result.card)
        self.assertEqual(result.card.owner, "u1")
        self.assertEqual(result.card.opportunity_id, "a")
        self.assertEqual(len(self.store.task_cards()), 1)
        self.assertIn("✅ Claimed by u1", format_claim_confirmation(result, NOW))

    def test_double_claim_returns_already_claimed_without_duplicate(self):
        first = self.store.claim("u1", "a", NOW)
        second = self.store.claim("u1", "a", NOW + timedelta(minutes=5))
        self.assertEqual(second.status, "already_claimed")
        self.assertEqual(second.card, first.card)
        self.assertEqual(len(self.store.task_cards()), 1)
        self.assertIn(
            "already claimed by you",
            format_claim_confirmation(second, NOW),
        )

    def test_different_user_can_claim_same_opportunity(self):
        self.store.claim("u1", "a", NOW)
        result = self.store.claim("u2", "a", NOW)
        self.assertEqual(result.status, "claimed")
        self.assertEqual(len(self.store.task_cards()), 2)

    def test_claim_expired_is_rejected_without_card(self):
        store = ClaimStore([opp("old", "Gone", NOW - timedelta(hours=1))])
        result = store.claim("u1", "old", NOW)
        self.assertEqual(result.status, "expired")
        self.assertIsNone(result.card)
        self.assertEqual(store.task_cards(), [])

    def test_claim_unknown_is_rejected_without_card(self):
        result = self.store.claim("u1", "nope", NOW)
        self.assertEqual(result.status, "unknown")
        self.assertIsNone(result.card)
        self.assertEqual(self.store.task_cards(), [])

    def test_duplicate_opportunity_ids_rejected(self):
        with self.assertRaises(ValueError):
            ClaimStore([opp("a", "One", NOW), opp("a", "Two", NOW)])


class TestSummaryAndPingSelector(unittest.TestCase):
    def test_end_of_day_summary_sections(self):
        store = ClaimStore(
            [
                opp("a", "Alpha", NOW + timedelta(days=2)),
                opp("b", "Beta", NOW + timedelta(days=5)),
                opp("c", "Gamma", NOW - timedelta(days=1)),
            ]
        )
        store.claim("u1", "a", NOW)
        text = store.end_of_day_summary(NOW + timedelta(hours=12))
        self.assertIn("Claimed:", text)
        self.assertIn("✅ Alpha — u1", text)
        self.assertIn("Still open:", text)
        self.assertIn("○ Beta", text)
        self.assertIn("Expired unclaimed:", text)
        self.assertIn("✕ Gamma", text)

    def test_end_of_day_empty_state(self):
        store = ClaimStore([])
        text = store.end_of_day_summary(NOW)
        self.assertIn("Nothing to report today.", text)

    def test_end_of_day_no_claims_message(self):
        store = ClaimStore([opp("a", "Alpha", NOW + timedelta(days=2))])
        text = store.end_of_day_summary(NOW)
        self.assertIn("No claims yet today", text)

    def test_due_within_48h_boundaries(self):
        store = ClaimStore(
            [
                opp("now", "DueNow", NOW),
                opp("edge", "Due48h", NOW + timedelta(hours=48)),
                opp("late", "Due48hPlus", NOW + timedelta(hours=48, seconds=1)),
                opp("far", "Due72h", NOW + timedelta(hours=72)),
            ]
        )
        for opp_id in ("now", "edge", "late", "far"):
            store.claim("u1", opp_id, NOW)
        due = store.due_within_48h(NOW)
        titles = [c.title for c in due]
        self.assertEqual(titles, ["DueNow", "Due48h"])

    def test_due_within_48h_excludes_unclaimed_and_expired(self):
        # Unclaimed opportunities have no owner, so they are never pinged.
        unclaimed = ClaimStore([opp("soon", "Soon", NOW + timedelta(hours=10))])
        self.assertEqual(unclaimed.due_within_48h(NOW), [])
        # An expired opportunity cannot be claimed, so it can never appear
        # in the ping list either.
        expired_store = ClaimStore([opp("past", "Past", NOW - timedelta(hours=1))])
        self.assertEqual(
            expired_store.claim("u1", "past", NOW).status, "expired"
        )
        self.assertEqual(expired_store.due_within_48h(NOW), [])
        # And a claimed task due soon IS pinged.
        claimed = ClaimStore([opp("soon", "Soon", NOW + timedelta(hours=10))])
        claimed.claim("u1", "soon", NOW)
        self.assertEqual(
            [c.title for c in claimed.due_within_48h(NOW)], ["Soon"]
        )


if __name__ == "__main__":
    unittest.main()
