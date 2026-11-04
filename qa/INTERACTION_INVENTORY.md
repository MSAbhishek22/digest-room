# Interaction Inventory — Digest Room (PLANNED controls; product NOT built)
Every row is BLOCKED until the control exists and is tested. No row claims PASS.
| Page/route | Control | Action | Expected behaviour | Test evidence | Status |
|---|---|---|---|---|---|
| Room timeline | ✅ reaction on digest item | Click/tap | Claim recorded once; agent confirms in thread; task card appears in rail | none yet | BLOCKED |
| Room timeline | Task card in rail | Click | Opens thread for that claim | none yet | BLOCKED |
| Room timeline | Message composer | Type + send | Message posts, appears in timeline, timestamped | none yet | BLOCKED |
| Room timeline | /digest command | Type + send | Agent re-posts digest on demand | none yet | BLOCKED |
| Room timeline | Retry (on agent error) | Click | Agent retries the failed action once; failure shown if it fails again | none yet | BLOCKED |
| Room list | Room switcher | Click | Timeline switches rooms; unread state clears | none yet | BLOCKED |
| Tasks rail | Collapse rail | Click | Rail hides; timeline widens; state persists for the session | none yet | BLOCKED |
| Settings | Agent on/off toggle | Toggle | Agent pauses/resumes posting; state shown in room header | none yet | BLOCKED |
Rules: no href="#", no dead buttons, no fake success toasts in the release. Any control
not implemented by Nov 7 must be removed from the release UI, not shipped decorative.

## Update 2026-11-04 — local harness controls (NOT Switch-room controls)
Tested over HTTP in tests/test_switch_adapter.py, 23/23 suite pass:
- Depth pipeline stage click / Enter / Space -> live count detail shows
  (stageDetail); reduced-motion -> flat list, no motion, actions still work
- Pipeline counts move on claim (verified by test + live curl QA)
- ✅ claim button in harness UI -> one task card, double claim = 1 card
- /switch/event ✅ reaction -> claim; ❤️ / message edit / empty user = no-op, 0 cards
- /api/tasks, /api/summary, /api/digest all return real store state
Real Switch-room rows above stay BLOCKED until the Mattermost room runs
and the same sequence is clicked there, on camera, for the demo video.
