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

## 1A. Docker nahi chalta ho to — official alternative (2026-11-04)
Switch's own quickstart lists, in this order: Docker Desktop, Rancher
Desktop, or Docker via Homebrew — and on Windows: Docker Desktop OR
Rancher Desktop. Rancher Desktop is free, open source, and gives
Switch Console a Docker-compatible daemon to talk to.
Steps (laptop, user):
1. Docker Desktop ko band/uninstall karo (dono ek saath clash karte hain).
2. Rancher Desktop install karo (rancherdesktop.io, Windows).
3. Setup me container runtime **dockerd (Moby)** chuno — containerd
   wala option nahi, kyunki Switch Console Docker daemon dhoondhta hai.
4. Rancher Desktop ko poora start hone do (tray icon ready), phir
   Switch Console kholo aur Add a server -> local server try karo.
5. Agar Rancher bhi "Docker daemon not found" ya WSL/virtualization
   error de, to problem Docker brand nahi hai — Windows me
   virtualization ya WSL band hai. Us case me koi bhi local container
   runtime nahi chalega, aur rasta badal jata hai: Switch server ko
   ek remote Linux host par chalana (Switch Console me SSH host
   onboard karke), jo Docker wale host par chalta hai. Free host
   dhoondhna (bina card ke) alag kaam hai — card manga to rukna hai.
   Isliye pehle Rancher try karo, aur jo exact error aaye wo bata do:
   error message + Windows 10 ya 11 — usse agla step decide hoga.
Why not "Docker ke bina source se chalao": Switch server ek stack
hai — switch-core (Python/FastAPI) + PostgreSQL + Gateway (Node) +
Mattermost — sab Docker Compose me bandhe hain. Laptop par bina
container ke ye stack haath se chalana practical nahi hai, aur
deadline 7 Nov tak usme time jaana risk hai. Rancher hi seedha rasta hai.

## 1B. Laptop par Rancher bhi na chale to — cloud solution (2026-11-04, researched, NOT deployed yet)
User ne 2026-11-04 ko bola laptop par Rancher wala rasta nahi chal sakta, isliye cloud dekha gaya. Result:
- **Railway ka official Agent Switch template sabse seedha cloud rasta hota** (switch + postgres + mattermost + setup + agents, ek click me, laptop ka Docker ya laptop on rehna zaroori nahi). Lekin **abhi free route BLOCKED hai**: Railway ne 2 Nov 2026 ko signups dobara khole, par naye customers ko deploy se pehle paid plan (Hobby/Pro) subscribe karna padta hai, free trial deploy temporarily unavailable hai. Free-only rule ke hisab se Railway par abhi deploy nahi karna — sirf tab jab free trial deploy wapas aaye.
- **Primary cloud route: GitHub Codespaces (free tier, bina card ke).** Personal account ko 120 core-hours/month milte hain; 2-core machine par ye ~60 wall hours hote hain — demo sessions ke liye kaafi hai, bas kaam khatam hone par codespace stop karna hai. Codespace ek Linux machine hai jisme Docker-in-Docker chalta hai, isliye Switch ka upstream docker-compose stack seedha uske terminal me chal sakta hai (Console ke SSH-host onboarding par bharosa nahi karna — Codespace ka SSH GitHub relay se hota hai, seedha port 22 nahi). Ports forwarded URL se khulenge: Mattermost room + Switch dashboard browser me.
- **Bachne wale raste:** Oracle/AWS/GCP free tier card mangte hain (rule ke bahar); Azure for Students $100 bina card ke deta hai par college-email verification me time lagega, 7 Nov deadline ke liye risky; GratisVPS/VPSWala free (1 vCPU, 1–2 GB) Switch stack ke liye kamzor hain.
- **Bacha hua tukda (host se alag):** agent ka subscription/API key abhi bhi user ka hai — Switch ko Claude Code, Codex ya OpenCode chahiye, aur wo laptop par ho ya cloud agent machine par, uska sign-in user ka apna hoga.
- Codespace steps (user ke GitHub se, deploy se pehle approval chahiye): digest-room ya switch repo se codespace banao (2-core), terminal me Switch repo ka deploy/local/docker-compose.yml chalao, Mattermost + Switch dashboard ke forwarded URLs kholo, "Digest Room" banao, agent enroll karo, phir section 3 ka workflow chalao.
- **UPDATE 2026-11-04 ~16:45 IST — STACK UP, koi card/payment nahi:** Codespace "opulent bassoon" (https://opulent-bassoon-7v9qgpg6vx7qfrgg9.github.dev/), sandbox-quantum/switch main, 2-core, Southeast Asia. Docker 29.9.2, Compose v5.6.1. `just` nahi tha, isliye cp .env.example .env + generate-env-secrets.sh fallback chala; GATEWAY_ADMIN_EMAIL=msabhishekbdps@gmail.com, SWITCH_VERSION=latest. Standalone stack (profiles collab + gateway, source build nahi, published images) up: gateway Up 3000, mattermost Up healthy 8065, postgres Up healthy 5432, switch Up 8000; curl teenon port par 200. Forwarded URLs (Public): API https://opulent-bassoon-7v9qgpg6vx7qfrgg9-8000.app.github.dev/, Gateway https://opulent-bassoon-7v9qgpg6vx7qfrgg9-3000.app.github.dev/, Mattermost https://opulent-bassoon-7v9qgpg6vx7qfrgg9-8065.app.github.dev/. Gateway password Codespace ke andar /workspaces/switch/.env me GATEWAY_ADMIN_PASSWORD= line par hai — chat me nahi likha gaya. Abhi tak koi room, agent ya Mattermost account verify nahi hua, kuch submit nahi hua. Codespace stop karne se pehle video record kar lena — inactivity par codespace ruk sakta hai.
- **UPDATE 2026-11-04 ~19:59 IST — ROOM + AGENT + MACHINE DONE, provider pending, Mattermost sign-in FAILED:** Gateway sign-in OK (System healthy). Digest Room Gateway se bana, Public, Mattermost bridge, URL https://opulent-bassoon-7v9qgpg6vx7qfrgg9-3000.app.github.dev/rooms/49a442a7-ee9c-41cc-8668-cca108e5eefd, Instructions field me poora digest prompt verified. Agent ka naam spaces ki wajah se "Digest Room agent" nahi rakh sakta tha — registered naam digest-room-agent (external), room me invited, Idle; agent page https://opulent-bassoon-7v9qgpg6vx7qfrgg9-3000.app.github.dev/agents/be762e44-9082-4c14-bd21-e139e21a7d42. Machine codespaces-2e4442 Connected (linux x64, Controller 0.31.1-dev.292.g4b29761, Agents running 0/0); enrolment ke liye Codespace .env me FEATURE_FLAGS_ENABLED=agent_management aur CONTROLLER_TOKEN_SECRET generate kiya gaya (values chat me nahi). **Mattermost sign-in FAILED:** seeded user aur admin dono se "email/username or password is invalid" (13:58–13:59 UTC), jabki setup logs kehte hain team + accounts exist karte hain — isliye 'switch' team Mattermost UI me verify nahi hui. Room Gateway se bana hai, isliye room exist karta hai, par Mattermost chat UI ka rasta abhi unresolved hai — password reset / account fix ke liye alag authorisation chahiye. Provider: Machines page par koi provider installed/signed-in nahi (Codex, Claude Code, Antigravity, Cursor CLI, OpenCode sab Not installed) — provider + subscription/API-key ka faisla user ka baaki hai, uske bina agent kaam nahi karega.
- **UPDATE 2026-11-04 ~20:55 IST — Mattermost FIXED, OpenCode detected, local model FAIL, free API key baaki:** Mattermost mmctl --local se seeded user ka password reset hua (naya value sirf Codespace .env me), API login 200, web sign-in OK — team "Switch" load hoti hai, channels Digest Room / Town Square / Off-Topic dikhte hain: https://opulent-bassoon-7v9qgpg6vx7qfrgg9-8065.app.github.dev/switch/channels/town-square. Ollama chal raha hai (localhost:11434), qwen2.5:3b aur qwen3:4b pull hue, Ollama test prompt ~18s me jawab deta hai — local model slow nahi hai. Par OpenCode 1.19.5 dono models par "Unexpected server error" deta hai, config fix karne ke baad bhi, log me detail nahi — isliye OpenCode + local Ollama Switch ke through abhi kaam nahi kar raha. Machines page par ab OpenCode 1.19.5 detected hai (controller restart + PATH fix ke baad), baaki providers Not installed. digest-room-agent abhi bhi external, Passive, Tools 0 / Models 0, Managed agents 0 — isko provider se link karne ke liye managed agent chahiye hoga, external agent ko seedha link nahi kar sakte. Agla step: user khud ek free-tier API key banaye (bina card ke) — Gemini (Google AI Studio), Groq, ya OpenRouter me se ek — key chat me kabhi nahi, sirf secure entry se. Uske baad OpenCode ko us provider par configure karke managed agent banega. Koi payment/card/paid provider nahi liya gaya, koi demo digest post nahi hua.
- **UPDATE 2026-11-05 ~10:36 IST — Gemini key BAN GAYI, managed agent BAN GAYA, par agent abhi jawab nahi de raha (2 user-only steps baaki):** Codespace/stack restart OK (Gateway/Mattermost/API 200). Google AI Studio me msabhishekbdps@gmail.com se ek free Gemini API key ban gayi, bina card/billing ke — key ki value kahin report/chat me nahi hai, sirf AI Studio me hai. Managed agent digest-room-managed ban gaya (OpenCode CLI, repo /workspaces/switch, addressing Open), Digest Room me invited hai, room instructions us par lagu hain. Par test message (10:35 IST) ka koi jawab nahi aaya — sirf join greeting dikhi; Gateway par "Not currently connected to this room / No session", 0 models. Do wajah: (1) OpenCode me key configure nahi hui — VS Code Web ne browser agent ko clipboard paste karne se mana kar diya, aur agent key type nahi kar sakta, isliye key paste karna user ka kaam hai (AI Studio tab se copy karke Codespace terminal me `opencode auth login` par paste); (2) Machine codespaces-2e4442 Disconnected/Offline dikh rahi hai (last seen 4 Nov 9:36 PM IST) — Codespace restart ke baad controller process khatam ho gaya, Gateway me Machines > Add machine se fresh enrollment code lekar Codespace terminal me controller dobara chalana hoga, tabhi machine Connected hogi aur models fetch honge. In dono ke baad hi room me test reply aayega, phir demo digest/claim workflow hoga. Koi payment/card nahi, koi demo digest post nahi hua, kuch submit nahi hua.
- **UPDATE 2026-11-05 ~11:40 IST — Copilot Free + OAuth DONE, machine ONLINE, par agent ko abhi bhi model/session nahi:** Gemini key paste clipboard blocker ki wajah se impossible nikla (har paste route fail, permission prompt kabhi nahi aaya), isliye rasta badla gaya. Copilot Free pehle se active tha ($0, 0% of 2,000 completions / 50 premium requests used, bina card ke). OpenCode me GitHub Copilot OAuth device flow complete hua ("Login successful", auth list me 1 credential). Par OpenCode 1.19.5 Copilot models ko resolve nahi kar pata — gpt-4o, gpt-5-mini, gpt-5.3-codex, gemini-3.8-flash sab "Unexpected server error" / ProviderModelNotFoundError; `opencode models` me sirf OpenCode ke apne free models dikhte hain (beam-free, big-pickle, glm-5.3-flash-free, deepseek-v4.1-flash-free, aadi). Control test beam-free 18 min tak bina jawab ke chalta raha. Controller enrollment command terminal me type karke chalaya gaya (paste nahi), machine codespaces-2e4442 Connected since 11:34 AM, Providers: OpenCode 1.19.5. Mattermost re-test (11:36 AM) par digest-room-managed ne thread me jawab diya — par sirf ye ki uska koi session nahi hai aur operator ko `opencode --prompt "connect to switch room Digest Room..."` chalana chahiye. Gateway par agent: OpenCode CLI, Session Addressable, Auto Session off, SESSIONS 0 LIVE / 0, MODELS 0, TOOLS 9. Agla step: pehle koi free model dhoondhna jo OpenCode me jawab de (glm/deepseek free), phir Auto Session on ya connect command se session banana. Controller Terminal 4 me foreground me chal raha hai — terminal band karne se machine phir offline ho jayegi. Koi payment/card nahi, koi demo digest nahi, kuch submit nahi hua.
- **UPDATE 2026-11-05 ~11:57 IST — OpenCode ke apne free models ka limit KHATAM, 18h wait nahi kar rahe:** beam-free 18 min, glm-5.3-flash-free 3 min, deepseek-v4.1-flash-free 3 min — teenon bina jawab ke latke, phir connect command par OpenCode ne bataya "Free limit reached / Free usage exceeded, subscribe to Go [retrying in 18h 6m]". Matlab ye teenon isiliye latke the ki OpenCode ki apni free allowance khatam ho gayi thi — kuch subscribe nahi kiya, koi payment nahi. Reset ~6 Nov 06:02 AM IST hota, par wait nahi kar rahe. Auto Session ON karke save kar diya gaya (badge dikhta hai), par usse koi session nahi bana; Gateway agent page par model picker hi nahi hai (MODELS 0). Connect command Big Pickle (default model) se chala, turant free-limit par atak gaya, Terminal 6 kill kar diya gaya; Terminal 4 (controller) chalta raha. Re-test message 11:51 AM par room me post hua, 11:56 AM tak koi jawab nahi. **Naya rasta (11:57 IST, chal raha hai):** Gemini key ko clipboard se paste karne ki jagah keyboard se TYPE karke `opencode auth login` (Google provider) me daalna — Gemini alag provider hai, uski apni free tier hai, OpenCode ke free limit se uska koi lena-dena nahi. Key ki value kahin report/chat me nahi aayegi, sirf OpenCode ke auth config me rahegi. Uske baad connect command + room re-test. Koi payment/card nahi, koi demo digest nahi, kuch submit nahi hua.
- **UPDATE 2026-11-05 ~16:10 IST — LOOP COMPLETE in the real room; reaction gap + turn-error remedy proven; video recording blocked in live browser:** Gemini key type karke `opencode auth login` me daali gayi (clipboard nahi), model google/gemini-3.5-flash-lite jawab deta hai (12:05 IST "Hello there!"). Gateway-native naya managed agent digest-room-managed-2 banaya gaya (Machines > New managed agent, OpenCode, Gemini 3.5 Flash Lite, addressing Open) — BOUND + LIVE (Agents running 1/1, SESSIONS 1 LIVE / 1, ROOMS 3 Live). Purana digest-room-managed kabhi bind nahi hua, side me pada hai, delete nahi kiya. Morning digest 3:19 PM IST room me post hua (3 DEMO items), us par real ✅ reaction lagi (~3:25 PM, count 1) — **par agent tak reaction ka event pahuncha hi nahi** (session me reaction ke baad zero parts): is Switch build me ✅ reaction events agent session tak forward nahi hote — Gateway room settings me aisa koi option nahi hai, aur repo me core/switch_core/transport/port.py:46 par on_reaction slot hai par Mattermost adapter/delivery usko call hi nahi karta — pure-reaction claim ke liye bridge me CODE change chahiye, setting nahi. Workaround: @mention se agent ko reaction ke baare me bataya gaya. Phir agent ke turns marne lage (reasoning ke baad 0 output tokens; error "Requests ending with a model turn are not supported") — 3:33 PM nudge aur 3:42 PM EOD request dono fail hue. **Managed agent restart (3:51 PM) ne error clear kar diya:** 3:53 PM wale turn me agent ne dono pending kaam poore kiye — in-thread claim confirmation 3:53:59 PM ("[2026-11-05T09:00:00Z] ✅ Claimed by user: DEMO — Approve vendor invoice batch (due Saturday 2026-11-07 03:16 IST). Task card created." — timestamp prefix 09:00 UTC hai, asli time nahi; naam "user" dikhta hai) aur EOD summary 3:53:59 PM (claimed invoice batch; still open launch checklist + client demo slot; expired None; 48h ping invoice batch ke liye). **Lesson:** channel padhne se pehle hamesha FRESH NAVIGATION karo — hard reload se bhi is tunnelled tab me naye posts nahi dikhe. **Video:** live browser se screen recording possible nahi hai (sirf still screenshots; Codespace me recorder/display nahi) — isliye Codespace ke andar recorder stack install karke (Xvfb + ffmpeg + real browser) record karne ki ek bounded try chal rahi hai; agar wo fail hui to user apne laptop se record karega (link + shot list). Koi payment/card nahi, kuch submit nahi hua.

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
