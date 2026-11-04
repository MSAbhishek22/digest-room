# Deployment Runbook — Digest Room (PRE-RELEASE; no deployment exists yet)
- Intended shape: Switch self-hosted by the user (Docker on own machine) + Mattermost
  bundled by Switch — per the official FAQ, no Slack workspace/admin access needed.
- This is NOT a public HTTPS deployment and must never be presented as one. The
  hackathon's own demo is a recording of the real running room, not a public URL claim.
- Harness-only public option (NOT deployed, user signup required): Render free
  tier, `render.yaml` at repo root, start `python3 -m digest_room.room_server`
  (reads $PORT, binds 0.0.0.0). Stop at once if Render asks for a card.
  A deployed harness is still NOT a Switch room and must never be
  submitted as the Switch demo.
- Env vars (names only, never values): PORT (Render sets it), SWITCH_HOST,
  AGENT_API_KEY_NAME (provider chosen at build time; bring-your-own agent
  subscription — no new purchase without approval).
- Health check (harness, verified locally 2026-11-04): GET / returns the
  room UI, GET /api/digest + /api/pipeline return live store state,
  POST /switch/event ✅ round-trips to one task card.
- Rollback: stop the Render service / stop the local server; no data is
  persisted (in-memory store), so rollback is a restart with an empty room.
