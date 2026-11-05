# Demo Video Manifest — Digest Room (NOT RECORDED YET)

Rule (user's video rule, non-negotiable): the submission video must be
a screen recording of the ACTUAL LIVE room working, with at least one
real action in it. Local-only video is an internal draft only and must
NEVER be submitted as a live demo. Screenshots/slides assembled as a
video are banned for the same reason.

## Target
- Length: 60–90 seconds, one continuous take
- Source: the real Switch + Mattermost room running in the GitHub Codespace ("opulent bassoon"), NOT the user's laptop, NOT the local harness
- Audio: none required; readable on-screen text carries it
- Secrets: none visible — no tokens, keys, or personal inboxes

## Shot list (in order, no cuts that hide a step)
The loop already ran live 2026-11-05 (digest 3:19 PM, claim confirmation 3:53 PM, EOD summary 3:53 PM), so the video is a one-take walkthrough of the completed live run in the real room — no re-run, no new posts:
1. (0–20s) Room opens. Morning digest readable: three DEMO items, deadline, prize, fit note, plus the ✅ reaction on it.
2. (20–45s) Thread on the digest opens. In-thread claim confirmation readable, with timestamp.
3. (45–70s) Back to channel. End-of-day summary readable: claimed / still open / expired, plus the 48h ping.
4. (70–90s) One line on screen: "Switch is the room. No room, no workflow."
The harness depth-pipeline / claimed-tasks-rail shots from the original list do NOT exist in Mattermost and are not filmed or implied.

## Recording method (2026-11-04 update, revised 2026-11-05)
Video is made by the assistant with a real screen recording
(Xvfb + Chromium + ffmpeg in the sandbox, tested pipeline), NOT by
assembling text cards / screenshots — the user's video rule bans
that feel for submission. The recording target is the real Switch
room only. A harness recording, if made as a rehearsal, is labelled
LOCAL DRAFT ONLY and is never submitted as a Switch demo.
2026-11-05 16:13 IST correction: the live browser cannot screen-record
at all (still screenshots only), and the Codespace had no recorder or
display — so the recording attempt now installs the stack INSIDE the
Codespace (Xvfb + ffmpeg + real browser) and records the live room
there. If that fails, the fallback is the user recording their own
screen from the live room link. The video is a walkthrough of the
completed live run (digest 3:19 PM, claim confirmation 3:53 PM, EOD
summary 3:53 PM, 5 Nov 2026) in one continuous take.

## Verification (fill only after recording)
- production_url / room: real Switch room in Codespace "opulent bassoon", Mattermost Digest Room channel (localhost:8065/switch/channels/digest-room), stack recovered 2026-11-05 ~8:00 PM IST after Docker RWLayer corruption (3 containers removed, volumes kept, all 4 services healthy 200)
- video_url: https://www.youtube.com/watch?v=c6ygxZTKrz0 (Public, channel MS Abhishek, published 2026-11-05; title "Digest Room — Flip the Switch (Best Business Workflow)")
- recorded_from_live_room: YES — one continuous ffmpeg x11grab take, display :99, 1280×720, 30 fps, h264; file submission/flip-switch-demo.mp4 (1,188,288 bytes); ffprobe duration 60.6 s (60–90 s required); nothing new posted in the room, nothing uploaded
- watched_back_link_opens: YES — link opened 2026-11-05 ~20:22 IST, page live with the exact title and description (repo link included); duration shown 1:00 on the watch page, 1:01 in Studio, consistent with the 60.6 s file
- duration_seconds: 60.6
- Honest warts (do not hide): ~20 s shows a "Loading..." spinner mid-take (channel reloading); the thread shot shows the agent's reply footer, not the confirmation text itself — the claim is confirmed on screen by the EOD summary (Claimed: DEMO — Approve vendor invoice batch). The 3:42 PM turn-failure message is visible in the channel history, as it was in the room.

Do not fill any of these fields in advance.
