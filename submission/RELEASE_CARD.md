# Release Card — Digest Room (Flip the Switch)
| Deliverable | Evidence |
|---|---|
| Project identity | Digest Room; team chat workflow where an agent + humans triage work; design: "room is the desk" |
| Research | Official Flip the Switch page verified 2026-11-03 and 2026-11-04; Gate A 5/5 design references inspected (5th: GoCardless brand typography) |
| Live application | REAL SWITCH ROOM LIVE (Codespace, not always-on): Digest Room https://opulent-bassoon-7v9qgpg6vx7qfrgg9-3000.app.github.dev/rooms/49a442a7-ee9c-41cc-8668-cca108e5eefd — managed agent digest-room-managed-2 bound + live (SESSIONS 1 LIVE / 1, Gemini 3.5 Flash Lite). **Workflow loop COMPLETE in the real room 2026-11-05 3:53 PM IST:** morning digest 3:19 PM (3 DEMO items) → real ✅ reaction → in-thread claim confirmation 3:53 PM → end-of-day summary 3:53 PM (claimed / still open / expired + 48h ping). |
| GitHub | PUBLIC + VERIFIED: https://github.com/MSAbhishek22/digest-room, main, remote head 2e7e1e9 (pushed 2026-11-05 ~17:52 IST: loop-complete docs, 4 files; verified by list_commits). Local tree matches remote for these files; next push will carry video-manifest verification once the video exists. |
| Deployment | Render free harness deploy (digest-room-harness) STILL NOT live, no .onrender.com URL; harness is NOT a Switch room. Real room runs in the Codespace (stack healthy 2026-11-05, stops on inactivity). |
| UI quality | Constitution + registry comparison written; harness UI built in constitution colours; real-room UI is Mattermost + Gateway |
| 3D experience | Exception REQUESTED, not approved; fallback plan documented (depth-layered CSS timeline) |
| Functional controls | Real-room workflow PROVEN 2026-11-05 3:53 PM: digest → ✅ reaction → in-thread confirmation → EOD summary, all in the live Mattermost room. Honest limits: this Switch build does not forward ✅ reaction events to agent sessions (on_reaction slot exists, nothing calls it), so the in-thread confirmation was triggered by an @mention nudge after the real ✅ reaction; agent turns can die with "Requests ending with a model turn are not supported" and a managed-agent restart clears it. |
| QA | 23/23 tests PASS on Linux sandbox 2026-11-05 (re-verified: Ran 23 tests, OK) — logic + harness; real-room workflow verified live 3:53 PM |
| Demo video | RECORDED from the real Switch room 2026-11-05 ~8:17 PM IST: one continuous take, 60.6 s, 1280×720, 30 fps, h264, 1.1 MB — file submission/flip-switch-demo.mp4; frames watched back (digest 5 s, thread 35 s, EOD summary 50 s/58 s). Honest warts: "Loading..." spinner ~20 s mid-take; thread shot shows the agent's reply footer, not the confirmation text itself (claim confirmed on screen by the EOD summary). |
| Published video | PUBLIC on YouTube 2026-11-05: https://www.youtube.com/watch?v=c6ygxZTKrz0 (channel MS Abhishek; title verified on the watch page; duration 1:00 watch page / 1:01 Studio; description with repo link verified) |
| Submission | REGISTERED 2026-11-04 ~16:25 IST: WeMakeDevs account created via GitHub sign-up (M S Abhishek, @MSABHISHEK22, msabhishekbdps@gmail.com, profile: M S / Abhishek, India, Student, Shobhit University, Meerut; DOB blank, email prefs unticked; age 18+ confirmed by user in chat), registration dialog answered Yes to the Keychron Keyboard giveaway, page shows "✓ REGISTERED" (count 7,109), dialog said "You're in. Here's 1 month of Wispr Flow free." (offer NOT taken, no confirmation number shown). LIMIT: registration dialog did NOT ask for team size, track, project name or repo, so Best Business Workflow / Digest Room / repo are NOT recorded against the entry yet — they go in the separate "Submit your project" step, not yet taken. Switch repo STARRED + verified same day. Discord join is user's tap, NOT confirmed. Deadline 7 Nov 2026 23:59 IST (safe 7 Nov 20:00 IST) |

## Status summary
- LIVE_DEPLOYMENT: IN_PROGRESS (real Switch room live in Codespace, not always-on; Render harness deploy still not live)
- GITHUB_COMMIT_MATCH: PARTIAL (remote public at 1a4cab2; local doc updates pending snapshot-push)
- ALL_VISIBLE_CONTROLS: PASS (real-room workflow proven end-to-end 2026-11-05 3:53 PM; honest limits: pure-reaction trigger is a platform gap, confirmation came via @mention nudge after the real ✅ reaction)
- 3D_EXPERIENCE: EXCEPTION_REQUESTED (needs user approval; rulebook allows APPROVED_EXCEPTION only after approval)
- UI_DISTINCTIVENESS: PASS (design documents + harness UI in constitution colours)
- RESPONSIVE_AND_ACCESSIBLE: PARTIAL (harness UI is single-column on mobile; real room untested)
- DEMO_VIDEO_RECORDED_FROM_LIVE: PASS (60.6 s one-take recording from the real room, 2026-11-05 ~8:17 PM IST, frames watched back)
- VIDEO_PUBLISHED_AND_URL_VERIFIED: PASS (Public, https://www.youtube.com/watch?v=c6ygxZTKrz0, link opened and verified 2026-11-05 ~20:22 IST)
- HACKATHON_RULE_COMPLIANCE: IN_PROGRESS (build inside Nov 4-7 window; registration DONE 2026-11-04, project submission pending)
- OVERALL_RELEASE: IN_PROGRESS (loop complete in real room; video recorded + published Public with verified link; only the "Submit your project" step outstanding)
## Gates
- A Research/design: PASS (5/5 references; 3D exception still unapproved)
- B Functional product: PASS — real Switch room + managed agent live, workflow loop completed 2026-11-05 3:53 PM
- C 3D/visual: BLOCKED (exception pending)
- D QA: PASS (23/23 logic/harness tests PASS; real-room workflow verified live)
- E GitHub/deployment: PARTIAL (public repo at 1a4cab2; doc updates pending push; Render harness not live)
- F Demo video: PASS (recorded from live room, 60.6 s; upload + link verification pending)
- G Final handoff: BLOCKED
