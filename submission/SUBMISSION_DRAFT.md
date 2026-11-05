# Submission draft — Digest Room (DO NOT SEND until the checklist is green)

Track: Best Business Workflow — Flip the Switch, WeMakeDevs x DevTools Academy x Switch
Team: Solo
Status 2026-11-05: SUBMITTED 2026-11-05 20:38 IST (see "Submission" below). Repo verified and registration DONE (see checklist); real Switch room live and workflow loop COMPLETE in it 2026-11-05 3:53 PM IST; demo video recorded from the live room and PUBLISHED Public at https://www.youtube.com/watch?v=c6ygxZTKrz0 (link opened + verified 2026-11-05 ~20:22 IST).

## Title
Digest Room — the morning triage your team already does, inside the chat room

## One line
A Switch room where an agent posts the morning digest, teammates claim
work with a ✅ reaction, and the day closes with a claimed / open /
expired summary — humans stay in charge of every register, submit, and pay tap.

## What to paste (after the video + repo exist)
- Repo: https://github.com/MSAbhishek22/digest-room (verified public, main, remote head 2e7e1e9, 2026-11-05)
- Demo video: https://www.youtube.com/watch?v=c6ygxZTKrz0 (Public, recorded ONLY from the real Switch/Mattermost room, 60.6 s)
- How Switch is used: Switch is the room itself. The agent posts the
  digest in the room, a ✅ reaction in the room is the claim, the
  agent confirms in-thread in the room, and the rail shows claimed
  tasks. Remove Switch and there is no workflow left.
- How to reproduce: clone the repo, run the test suite, run the
  harness, then follow switch/SWITCH_SETUP.md for the real room.
- What is NOT claimed: the local harness is not a Switch room, demo
  data is labelled DEMO, and the agent never registers, submits, or
  pays for anything. Honest limits of the demo: in this Switch build
  ✅ reaction events are not forwarded to agent sessions (the
  on_reaction handler exists but nothing calls it), so after the real
  ✅ reaction on the digest, the in-thread confirmation was triggered
  by an @mention nudge; agent turns can also fail with "Requests
  ending with a model turn are not supported" and a managed-agent
  restart clears it. The confirmation's timestamp prefix shows 09:00
  UTC rather than the actual post time, and the name shown is "user".

## Pre-send checklist (all must be true)
- [x] Registered on the official page (2026-11-04 ~16:25 IST: page shows "✓ REGISTERED", count 7,109; Keychron Keyboard giveaway entered = Yes) + repo starred (verified 2026-11-04)
- [ ] Discord joined (user's tap, link https://discord.gg/E2rWw2Yhsm — NOT confirmed)
- [x] Track (Best Business Workflow), project name (Digest Room) and repo entered — submitted 2026-11-05 20:38 IST via the "Submit your project" step; page shows "SUBMITTED" — "Digest Room" — "Solo entry · Flip the Switch Hackathon", filed by M S Abhishek @msabhishek22 on 5 Nov 2026, 20:38; no confirmation number or submission ID shown
- [x] Real Switch room running (Codespace "opulent bassoon"), workflow loop proven in it 2026-11-05 3:53 PM IST (digest → ✅ reaction → in-thread confirmation → EOD summary)
- [x] Public repo pushed, remote commit verified against local (remote head a089a23, verified 2026-11-05 ~20:22 IST)
- [ ] README shows Switch centrality (it does, in the table above)
- [x] Demo video recorded from the real room, uploaded, link opened and watched back (Public https://www.youtube.com/watch?v=c6ygxZTKrz0, verified 2026-11-05 ~20:22 IST)
- [x] Submission form sent before 7 Nov 2026, 23:59 IST (safe: 7 Nov 20:00 IST) — SENT 2026-11-05 20:38 IST, two days early

## Side tracks (free, optional, same project)
- Best Blog (AirPods 5): see submission/BLOG_DRAFT.md — publish only
  after the real room works, so the blog describes a real build.
- #HowISwitch (Logitech keyboard, top 5 posts): see submission/SOCIAL_DRAFT.md.
- Swag draw + certificate: automatic with a valid submission.
