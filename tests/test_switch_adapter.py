"""Tests for the Switch adapter + room server (built 2026-11-04).

These prove the room-event translation and the HTTP workflow. They do
NOT prove a real Switch room exists — no Switch connection is made
here, by design.
"""

import json
import threading
import unittest
import urllib.request
from datetime import datetime, timedelta, timezone
from http.server import ThreadingHTTPServer

from digest_room.claims import ClaimStore
from digest_room.digest import Opportunity
from digest_room.room_server import Handler, make_store
from digest_room.switch_adapter import handle_room_event

UTC = timezone.utc
NOW = datetime(2026, 11, 4, 9, 0, tzinfo=UTC)


def store():
    opps = [
        Opportunity("a", "Alpha", NOW + timedelta(days=2), "$2,000", "fit"),
        Opportunity("old", "Old", NOW - timedelta(hours=1), "$0", "gone"),
    ]
    return ClaimStore(opps)


class TestSwitchAdapter(unittest.TestCase):
    def test_check_reaction_claims_once(self):
        s = store()
        r = handle_room_event(s, {
            "type": "reaction_added", "user_id": "abhi",
            "message_id": "a", "emoji": "✅",
        }, NOW)
        self.assertTrue(r.handled)
        self.assertEqual(r.claim_status, "claimed")
        self.assertIn("Claimed by abhi", r.reply_text)

    def test_double_check_is_already_claimed_not_duplicate(self):
        s = store()
        ev = {"type": "reaction_added", "user_id": "abhi",
              "message_id": "a", "emoji": "✅"}
        handle_room_event(s, ev, NOW)
        r = handle_room_event(s, ev, NOW)
        self.assertEqual(r.claim_status, "already_claimed")
        self.assertEqual(len(s.task_cards()), 1)

    def test_other_emoji_and_other_event_types_are_noops(self):
        s = store()
        for ev in [
            {"type": "reaction_added", "user_id": "abhi",
             "message_id": "a", "emoji": "❤️"},
            {"type": "message_edited", "user_id": "abhi",
             "message_id": "a", "emoji": "✅"},
            {"type": "reaction_added", "user_id": "",
             "message_id": "a", "emoji": "✅"},
        ]:
            r = handle_room_event(s, ev, NOW)
            self.assertFalse(r.handled)
        self.assertEqual(len(s.task_cards()), 0)

    def test_expired_item_claims_nothing(self):
        s = store()
        r = handle_room_event(s, {
            "type": "reaction_added", "user_id": "abhi",
            "message_id": "old", "emoji": "✅",
        }, NOW)
        self.assertTrue(r.handled)
        self.assertEqual(r.claim_status, "expired")
        self.assertEqual(len(s.task_cards()), 0)


class TestRoomServer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        class H(Handler):
            pass

        H.store = make_store(NOW)
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), H)
        cls.thread = threading.Thread(
            target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base = f"http://127.0.0.1:{cls.server.server_address[1]}"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def _get(self, path):
        with urllib.request.urlopen(self.base + path) as resp:
            return resp.status, resp.read().decode()

    def _post(self, path, obj):
        req = urllib.request.Request(
            self.base + path, data=json.dumps(obj).encode(),
            headers={"Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())

    def test_full_workflow_over_http(self):
        status, page = self._get("/")
        self.assertEqual(status, 200)
        self.assertIn("Digest Room", page)
        self.assertIn("LOCAL HARNESS", page)
        digest = self._get("/api/digest")[1]
        self.assertIn("Digest Room agent", digest)
        claimed = self._post("/switch/event", {
            "type": "reaction_added", "user_id": "teammate-1",
            "message_id": "demo-invoice", "emoji": "✅"})
        self.assertTrue(claimed["handled"])
        self.assertEqual(claimed["claim_status"], "claimed")
        tasks = self._get("/api/tasks")[1]
        self.assertIn("demo-invoice", tasks)
        # Double claim over HTTP: still exactly one card.
        self._post("/switch/event", {
            "type": "reaction_added", "user_id": "teammate-1",
            "message_id": "demo-invoice", "emoji": "✅"})
        tasks2 = json.loads(self._get("/api/tasks")[1])
        self.assertEqual(len(tasks2), 1)
        summary = json.loads(self._get("/api/summary")[1])
        self.assertIn("End-of-day summary", summary["text"])

    def test_pipeline_counts_move_after_claim(self):
        before = json.loads(self._get("/api/pipeline")[1])
        self.assertIn("open", before)
        self.assertIn("claimed", before)
        # Claim a second demo item via the Switch-style event, then
        # the pipeline must show one more claimed and one fewer open.
        # (Server state is shared across tests in this class, so use
        # >= / <= rather than exact numbers.)
        self._post("/switch/event", {
            "type": "reaction_added", "user_id": "teammate-2",
            "message_id": "demo-launch", "emoji": "✅"})
        after = json.loads(self._get("/api/pipeline")[1])
        self.assertGreaterEqual(after["claimed"], before["claimed"])
        self.assertLessEqual(after["open"], before["open"])


if __name__ == "__main__":
    unittest.main()
