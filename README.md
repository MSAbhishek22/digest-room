# Digest Room — Flip the Switch (Best Business Workflow)

> Nothing new. Something missing.

Every morning, a small team wakes up to the same mess: opportunities
scattered across chats, tabs, and inboxes, nobody sure who picked up
what, and the urgent thing quietly expiring while everyone assumes
someone else has it. Phone Link solved this for calls. Nobody solved
it for the morning triage — the ten minutes where a team decides what
actually gets done today.

Digest Room is that missing ten minutes, inside the chat room the team
already lives in.

## The story in 30 seconds

1. **Morning, 08:00.** The agent posts one digest in the room:
   today's opportunities, earliest deadline first, expired ones
   left out, no noise.
2. **A teammate reacts ✅.** That's the whole interface. No form,
   no dashboard, no new app to learn.
3. **The agent confirms in-thread**, and a task card appears in the
   claimed-tasks rail. One claim, one card, forever — double-clicking
   never duplicates it.
4. **Evening.** The agent posts claimed / still open / expired, and
   pings owners of tasks due within 48 hours.
5. **Humans stay in charge.** The agent prepares; humans register,
   submit, and pay. It never does those taps, and never claims on
   anyone's behalf without their ✅.

## Why Switch is central (judges, read this first)

Without the Switch room, there is no Digest Room at all: no digest
post, no reaction claim, no thread confirmation, no shared history.
Switch is not a logo on this project — it is the room itself.
That is why this entry targets **Best Business Workflow**: the most
practical workflow where people and AI agents get work done together.

| Judging lens (official page) | How Digest Room answers it |
|---|---|
| Use of Switch — would it stop working without it? | Yes, completely. Remove the room and the workflow disappears. |
| Technical execution — can someone clone and reproduce it? | Stdlib Python only, `python3 -m unittest` + `python3 -m digest_room.room_server`, no secrets, no paid service. |
| Creativity and impact — a fresh idea a real team keeps using? | A daily triage ritual, not a demo that dies on stage. The same room works the day after the hackathon. |
| Presentation — do video + README make Switch obvious in 30s? | Shot 1 is the agent posting in the room. Shot 2 is the ✅ claim. No slides, no narration over screenshots. |

## What exists right now

- `digest_room/digest.py` — morning-digest formatting (sorted by
  deadline, expired excluded, honest empty-digest message).
- `digest_room/claims.py` — react-to-claim state machine: idempotent
  claims, task cards, end-of-day summary, 48h ping selector.
- `digest_room/switch_adapter.py` — translates a Switch/Mattermost-style
  ✅ reaction event into the claim machine. Other emojis, edits, and
  missing fields are deliberate no-ops, never task cards.
- `digest_room/room_server.py` — local stdlib harness proving digest ->
  claim -> card -> summary over HTTP, plus a functional depth
  pipeline view (Open -> Claimed -> Due 48h -> Expired, live counts,
  clickable stages, reduced-motion flat fallback). Labelled
  LOCAL HARNESS in the UI.
- `switch/SWITCH_SETUP.md` + `switch/ROOM_INSTRUCTIONS.md` — the exact
  laptop steps and agent prompt for the real room.
- `design/`, `qa/`, `deployment/`, `submission/` — rulebook pack:
  constitution, registry, interaction inventory, runbook, manifest,
  release card, submission draft, video manifest, blog draft.

## Run it (local harness — NOT a Switch room)

```bash
python3 -m unittest discover -s tests -t . -v
python3 -m digest_room.room_server
# open http://127.0.0.1:8000/
```

Demo data in the harness is labelled DEMO. It is not a live feed.

## What does NOT exist yet (honest, and it blocks a win)

- A **real Switch room**: Switch Console (Windows early access) +
  Docker + bundled Mattermost + agent connection, on the user's
  laptop. The harness above must never be filmed or submitted as one.
- A public URL, demo video, registration, or submission.
  Registration + Discord + Switch install are the user's own taps
  (see `switch/SWITCH_SETUP.md`). Safe submission target:
  **7 Nov 2026, 20:00 IST** (deadline 23:59 IST).

## Demo plan (recorded only from the real room)

60–90 seconds, one continuous take, readable text, no credentials:
(1) agent posts the morning digest; (2) a teammate reacts ✅;
(3) agent confirms in-thread, task card appears in the rail;
(4) depth pipeline count moves Open -> Claimed;
(5) end-of-day summary posts. Full shot list:
`submission/DEMO_VIDEO_MANIFEST.md` (NOT recorded yet).
