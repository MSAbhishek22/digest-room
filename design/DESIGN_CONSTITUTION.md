# Digest Room — Design Constitution (Flip the Switch, Best Business Workflow)
Status: DESIGN ONLY, 2026-11-03. No product built yet; Gate A partial (see references).

## Personality and tone
Mission-control room, not a chatbot toy. Calm, precise, operator-like. The agent is a colleague
with a nameplate, not a mascot. Copy is short, factual, timestamped. No hype words in the room.

## User and context
A small team (1-4) in a chat room on their own machine, morning triage + end-of-day close.
Used on a laptop, often while multitasking. Every action must be readable at a glance.

## Central idea / visual metaphor
"The room is the desk." The chat timeline IS the workflow: digest post -> reaction claim ->
task card -> summary. No separate dashboard tab hiding the work. A slim right rail shows
claimed tasks only; the conversation stays the hero.

## Palette (semantic roles, not just hex)
- Room background: deep slate `#0F1419` — focus, night-shift console.
- Message surface: slate panel `#1A222C` — one step above background.
- Agent accent: signal lime `#A3E635` — reserved ONLY for agent actions (digest post, claim
  confirmation, summary). Humans never get lime, so agent work is instantly scannable.
- Human text: warm off-white `#E7E5E4`; secondary text muted slate `#94A3B8`.
- Urgency: amber `#F59E0B` for due-within-48h only. No red in normal use; red is reserved
  for a failed agent action (error state only).
- Borders: hairline `#2A3646`. No gradients, no glow, no glassmorphism.

## Typography
- UI + messages: system sans (Inter fallback) — chat must feel native, not designed-up.
- Agent labels + timestamps: monospace (JetBrains Mono fallback) — the "operator log" voice.
- Hierarchy: room title 20px semibold; message author 14px semibold; body 15px; timestamps
  12px mono muted. One size scale, no display type in the room.

## Layout and navigation
- Three columns max: room list (narrow) | message timeline (hero, 640px max readable width,
  centred) | claimed-tasks rail (280px, collapsible). Mobile: single column, rail becomes a
  bottom sheet. No hero section, no marketing landing inside the product.
- Information architecture: Rooms -> Timeline -> Thread (claim discussion) -> Task card.
  Nothing else. Settings is one screen, not a maze.

## Component behaviour
- Reaction claim: one click on ✅, immediate pressed state, agent confirmation appears in
  thread within seconds, task card appears in rail. Double-click must NOT double-claim
  (idempotency by message id + user id; duplicate claim shows "already claimed by you").
- Every agent message carries a visible timestamp + source label ("Digest Room agent").
- Loading: agent "working" indicator with elapsed seconds, never a fake instant reply.
- Empty state: "No claims yet today — react ✅ on a digest item to claim it."
- Error state: agent failure posts a red-bordered message with a Retry button; never a
  silent drop and never a fake success toast.

## Motion
- Restrained: message entry = 150ms fade+rise; rail card entry = same. No bounce, no
  floating blobs. `prefers-reduced-motion`: all entry motion off, content appears instantly.
  Motion never blocks the claim action.

## 3D / depth concept — IMPLEMENTED 2026-11-04, exception WITHDRAWN
The earlier exception request is withdrawn. Instead of a decorative room
diorama, the harness has a functional depth pipeline: Open -> Claimed ->
Due within 48h -> Expired unclaimed, laid out in CSS perspective
(nearest = open work, furthest = closed). Why it earns its place: an
operator sees in one glance where work is stuck — e.g. 3 open, 0 claimed
means nobody has picked anything up — without scrolling a flat list.
Each stage is clickable/keyboard-operable and shows its live count
from /api/pipeline; counts are never hardcoded. Fallback: with
prefers-reduced-motion or no JS, the same four stages appear as a flat
ordered list, and every workflow action still works from the timeline.
No WebGL, no spinning model, no motion that blocks a claim.

## Responsive and accessibility
- Desktop / tablet / mobile viewports; no horizontal overflow; touch targets >= 44px.
- Keyboard: Tab order follows timeline -> composer -> rail; focus ring always visible.
- Contrast: off-white on deep slate passes AA; lime used for labels, never for body text
  on white. All controls have accessible names; agent messages are announced as such.

## Design references inspected 2026-11-03
1. Slack (https://slack.com/) — same category (team chat). Inspected: homepage text +
   channel/agent/workflow descriptions. Learn: agent inside channels, "track/approve/complete
   without leaving the conversation". NOT copied: Slack's purple brand, marketing layout.
   Translated: our rail + in-thread claim confirmations.
2. Linear (https://linear.app/) — related category (agent workflows). Inspected: homepage
   activity-feed + agent workflow copy. Learn: "workflows shared by humans and agents",
   terse activity log entries with timestamps. NOT copied: Linear's dark marketing hero,
   issue-tracker layout. Translated: mono timestamp log voice for agent messages.
3. Three.js (https://threejs.org/) — 3D reference. Inspected: examples gallery listing.
   Learn: WebGL is powerful but heavy; a chat workflow does not earn that cost. Translated:
   the decision to request a 3D exception rather than bolt on decoration.
4. Mattermost (https://mattermost.com/) — same category, self-hosted chat. Inspected
   2026-11-03: homepage copy — searchable history across channels/threads, deploy
   anywhere including self-hosted/air-gapped. Learn: self-hosting is the privacy story
   itself, and channels + threads are the workflow spine. NOT copied: Mattermost's
   enterprise/security marketing tone. Translated: our self-host-first room design and
   thread-based claim confirmations.
5. GoCardless brand typography (https://brand.gocardless.com/typography) —
   typography/hierarchy reference. Inspected 2026-11-04: Inter as UI typeface
   designed for legibility at small sizes, with a focused weight set
   (400 body, 500 emphasis, 600 headings), one display heading per page,
   body lines kept to 65-75 characters, and hierarchy built from size +
   weight, not from extra typefaces. NOT copied: GoCardless brand voice or
   marketing scale (64px display). Translated: our existing scale stays
   (20px room title / 14px author / 15px body / 12px mono timestamps),
   Inter (system-sans fallback, no webfont dependency in the room) for UI,
   JetBrains Mono fallback only for agent labels + timestamps, and the
   640px readable timeline width already in this constitution — which
   matches the 65-75 character line rule at 15px body size.
   Gate A references are now 5/5 inspected 2026-11-04.
