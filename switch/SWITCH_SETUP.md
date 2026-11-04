# Switch room setup — Digest Room (user's laptop steps)

Status 2026-11-04: NOT DONE YET. This is the step that decides whether
the entry can win — without a real Switch room, there is no entry,
only a local harness. Do these in order, and stop at once if any step
asks for a card or payment (free-only rule).

## 0. Registration first (user tap, ~5 min)
1. Register on the official page: https://www.wemakedevs.org/hackathons/switch
2. Star the Switch repo (timeline step on that page).
3. Join the WeMakeDevs Discord (help channel for the whole event).
4. Solo entry is allowed; no team needed.

## 1. Install (Windows — early access, so expect friction)
- Switch Console is the desktop app. Official page: Console runs on
  macOS, with Windows and Linux builds in early access.
- Docker to run Switch on your own machine.
- An AI coding agent you already use: Claude Code, Codex, or OpenCode
  work out of the box through Switch Console.
- The official 10-minute quickstart is the one link to open first:
  docs.switchagents.ai (quickstart). If the Windows Console build
  blocks you, ask in the WeMakeDevs Discord before improvising a
  workaround — a fake room is worse than a delayed room.

## 2. Create the room
- Run Switch self-hosted on your machine. It comes with Mattermost,
  so no Slack workspace and no admin access are needed.
- Create a room named "Digest Room".
- Connect your agent to that room.
- Paste switch/ROOM_INSTRUCTIONS.md as the room's agent instructions.

## 3. Run the workflow in the real room (this is the demo)
1. Agent posts the morning digest in the room.
2. A teammate reacts ✅ on one item.
3. Agent confirms in-thread and a task card appears (rail / thread).
4. Agent posts the end-of-day summary.
5. Record that whole sequence, 60-90 seconds, one continuous take,
   readable text, no credentials visible. Record from the Mattermost
   room itself — never from the local harness in digest_room/,
   never from screenshots or slides.

## 4. What the local harness is for
`python3 -m digest_room.room_server` proves digest -> claim -> card ->
summary logic on any machine, including this Linux sandbox. It is a
dev harness only. If the Switch room cannot be made to run, the honest
status is BLOCKED, not "demo ready".

## 5. Submission checklist (before 7 Nov 2026, 23:59 IST)
- [ ] Registered + Discord joined
- [ ] Real Switch room running, workflow proven in it
- [ ] Public repo pushed (needs your explicit push approval)
- [ ] README shows Switch is central (it is: no room = no workflow)
- [ ] Demo video recorded from the real room, uploaded, link verified
- [ ] Best Blog side track (AirPods 5) — optional, free extra shot
- [ ] #HowISwitch post — optional, free extra shot
- [ ] Submission form sent before 7 Nov 23:59 IST (safe target: 7 Nov 20:00 IST)
