# Release Card — Digest Room (Flip the Switch)
| Deliverable | Evidence |
|---|---|
| Project identity | Digest Room; team chat workflow where an agent + humans triage work; design: "room is the desk" |
| Research | Official Flip the Switch page verified 2026-11-03; Slack/Linear/Three.js inspected 2026-11-03; 2 references still uninspected |
| Live application | NONE — local harness only; no Switch room, no public URL |
| GitHub | LOCAL COMMIT DONE b3c9f41 (23 files incl. MIT LICENSE); remote NOT created — connector create 403, browser creation in progress, push bundle verified at ~/workspace/hackathons/digest-room.bundle |
| Deployment | Runbook is pre-release only; no provider, no build, no URL |
| UI quality | Constitution + registry comparison written; harness UI built in constitution colours |
| 3D experience | Exception REQUESTED, not approved; fallback plan documented (depth-layered CSS timeline) |
| Functional controls | Harness controls tested (see below); real Switch-room controls BLOCKED until the room runs |
| QA | 22/22 tests PASS on Linux sandbox 2026-11-04 (17 scaffold + 5 adapter/server) — logic + harness only, NO real Switch room tested yet |
| Demo video | NONE — must be recorded from the real Switch/Mattermost room, never from the harness, never slides |
| Published video | BLOCKED_AUTHORIZATION (no video, no upload) |
| Submission | NOT registered; registration + Discord + Switch install are the user's taps; deadline 7 Nov 2026 23:59 IST |

## Status summary
- LIVE_DEPLOYMENT: BLOCKED (no Switch room; hackathon demo is a room recording, not a public URL)
- GITHUB_COMMIT_MATCH: BLOCKED (no remote repo)
- ALL_VISIBLE_CONTROLS: PARTIAL (harness controls tested; real room controls BLOCKED)
- 3D_EXPERIENCE: EXCEPTION_REQUESTED (needs user approval; rulebook allows APPROVED_EXCEPTION only after approval)
- UI_DISTINCTIVENESS: PASS (design documents + harness UI in constitution colours)
- RESPONSIVE_AND_ACCESSIBLE: PARTIAL (harness UI is single-column on mobile; real room untested)
- DEMO_VIDEO_RECORDED_FROM_LIVE: BLOCKED (no room running yet)
- VIDEO_PUBLISHED_AND_URL_VERIFIED: BLOCKED
- HACKATHON_RULE_COMPLIANCE: IN_PROGRESS (build now inside Nov 4-7 window; registration pending)
- OVERALL_RELEASE: IN_PROGRESS (workflow proven in harness; real Switch room, repo, video, submission all outstanding)
## Gates
- A Research/design: IN_PROGRESS (2 references uninspected; 3D exception unapproved)
- B Functional product: BLOCKED — build window Nov 4-7; building the workflow today would break hackathon rules. NON-Switch scaffold only (digest formatter + claim state machine + 17 tests) exists locally since 2026-11-03; Switch setup, room, agent connection, and workflow remain untouched.
- C 3D/visual: BLOCKED (exception pending)
- D QA: BLOCKED (no product to test)
- E GitHub/deployment: BLOCKED
- F Demo video: BLOCKED
- G Final handoff: BLOCKED
