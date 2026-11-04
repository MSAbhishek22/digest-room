# Blog draft — Best Blog side track (publish ONLY after the real room works)

Title: I gave my team's morning triage a room — and a ✅ became the whole interface

## The problem (nothing new, something missing)
Every morning our team did the same triage in three places at once:
a chat, a spreadsheet, and someone's memory. The urgent thing expired
quietly because everyone assumed someone else had picked it up.

## What I built
Digest Room, in a Switch room. The agent posts one digest at 08:00.
A teammate reacts ✅. The agent confirms in-thread and a task card
appears. At day's end, the agent posts claimed / open / expired and
pings owners due within 48 hours. No new app, no form, no dashboard
to learn — the room is the desk.

## What Switch actually did
Switch was not decoration. It is the room: the digest lives there,
the reaction lives there, the confirmation lives there, the history
lives there. Take Switch away and there is no workflow left. That
centrality is the whole point, and it is why the demo video shows
the room itself, not slides about it.

## What I learned (honest)
- A reaction is a better interface than a form when the team is
  already in chat — one tap, no context switch.
- Idempotency matters more than features: a double ✅ must never
  make a duplicate card, or trust in the room dies on day one.
- Windows Console is early access, so setup friction is real.
  The WeMakeDevs Discord is where that gets unblocked, not by
  pretending the room works when it doesn't.
- The agent prepares; humans register, submit, and pay. That line
  is not marketing — it is the guardrail that keeps an agent
  workflow trustworthy.

## Setup in brief
Switch Console + Docker, self-hosted, bundled Mattermost (no Slack
admin needed), agent connected to the room, room instructions from
this repo's switch/ folder. Full steps: switch/SWITCH_SETUP.md.

---
Status: DRAFT. Do not publish until the real room has run and the
demo video exists, so every sentence above describes a real build.
