"""Runnable Digest Room dev harness — stdlib only, no dependencies.

Run from the project root:
    python3 -m digest_room.room_server
    # then open http://127.0.0.1:8000/

This is a LOCAL harness that proves the full workflow end to end:
digest -> ✅ claim -> task card in rail -> end-of-day summary.
It is NOT a Switch room and must never be filmed or submitted as one.
The real demo is recorded from the Switch + Mattermost room on the
user's laptop (see switch/SWITCH_SETUP.md); this harness exists so the
workflow logic is proven before that room is wired up.

Demo data is labelled DEMO in the UI. It is not a live feed and not
a claim about any real hackathon, prize, or deadline.

Endpoints (JSON unless noted):
  GET  /                  room UI (deep slate + signal lime, per constitution)
  GET  /api/digest        current digest text + items
  POST /api/claim         {"user_id": ..., "opportunity_id": ...}
  POST /switch/event      Switch-style reaction event (see switch_adapter)
  GET  /api/tasks         claimed task cards
  GET  /api/summary       end-of-day summary text
"""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

from digest_room.claims import ClaimStore
from digest_room.digest import Opportunity, format_digest
from digest_room.switch_adapter import handle_room_event

NOW = datetime.now(timezone.utc)


def demo_opportunities(now: datetime) -> list[Opportunity]:
    return [
        Opportunity(
            id="demo-invoice",
            title="DEMO — Approve vendor invoice batch",
            deadline=now + timedelta(hours=36),
            prize="Team ops",
            fit_note="Needs one human approval; agent prepares the batch.",
        ),
        Opportunity(
            id="demo-launch",
            title="DEMO — Review launch checklist",
            deadline=now + timedelta(days=3),
            prize="Team ops",
            fit_note="Checklist owner still unclaimed.",
        ),
        Opportunity(
            id="demo-client",
            title="DEMO — Book client demo slot",
            deadline=now + timedelta(days=5),
            prize="Team ops",
            fit_note="Calendar hold needs a human to confirm.",
        ),
    ]


def make_store(now: datetime | None = None) -> ClaimStore:
    now = now or datetime.now(timezone.utc)
    return ClaimStore(demo_opportunities(now))


def pipeline_counts(store: ClaimStore, now: datetime) -> dict:
    """Counts for the depth pipeline view: open -> claimed -> due soon -> closed.

    This is why the depth view exists: an operator sees at a glance
    where work is stuck (many open, few claimed) instead of scrolling
    a flat list. Counts are computed from the live store, never hardcoded.
    """
    claimed = store.task_cards()
    claimed_ids = {c.opportunity_id for c in claimed}
    opps = list(store._opportunities.values())
    open_ops = [o for o in opps if o.id not in claimed_ids and not o.is_expired_at(now)]
    expired = [o for o in opps if o.id not in claimed_ids and o.is_expired_at(now)]
    return {
        "open": len(open_ops),
        "claimed": len(claimed),
        "due_within_48h": len(store.due_within_48h(now)),
        "expired_unclaimed": len(expired),
        "stages": ["open", "claimed", "due_within_48h", "expired_unclaimed"],
    }


def card_json(card) -> dict:
    return {
        "id": card.id,
        "opportunity_id": card.opportunity_id,
        "owner": card.owner,
        "title": card.title,
        "deadline": card.deadline.isoformat(),
        "claimed_at": card.claimed_at.isoformat(),
    }


PAGE = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Digest Room — local harness (NOT a Switch room)</title>
<style>
.pipeline{perspective:900px;display:flex;gap:12px;flex-wrap:wrap}
.stage{flex:1;min-width:140px;background:#1A222C;border:1px solid #2A3646;border-radius:8px;padding:12px;cursor:pointer;transition:transform 150ms ease}
.stage:nth-child(1){transform:translateZ(60px)}
.stage:nth-child(2){transform:translateZ(30px)}
.stage:nth-child(3){transform:translateZ(0)}
.stage:nth-child(4){transform:translateZ(-30px) scale(.97);opacity:.9}
.stage b{font-size:28px;color:#A3E635}
@media (prefers-reduced-motion: reduce){.stage{transform:none!important;transition:none}}
body{margin:0;background:#0F1419;color:#E7E5E4;font-family:Inter,system-ui,sans-serif}
.wrap{max-width:980px;margin:0 auto;display:grid;grid-template-columns:1fr 280px;gap:16px;padding:16px}
.panel{background:#1A222C;border:1px solid #2A3646;border-radius:8px;padding:16px}
h1{font-size:20px;margin:0 0 4px}.mono{font-family:ui-monospace,monospace;color:#94A3B8;font-size:12px}
.agent{color:#A3E635}.amber{color:#F59E0B}
button{background:#A3E635;border:0;border-radius:6px;padding:10px 14px;font-size:15px;min-height:44px;cursor:pointer}
button:disabled{opacity:.5}pre{white-space:pre-wrap;font-size:15px;line-height:1.5}
@media(max-width:700px){.wrap{grid-template-columns:1fr}}
</style></head><body><div class="wrap"><div class="panel">
<h1>Digest Room</h1><p class="mono">LOCAL HARNESS — not a Switch room. Demo data only.</p>
<pre id="digest">Loading digest…</pre>
<div id="items"></div>
<h2 style="font-size:16px">Workflow pipeline — depth view</h2>
<p class="mono">Nearest = open work, furthest = closed. Click a stage to see what it means. Flat list if motion is reduced.</p>
<div class="pipeline" id="pipeline"></div><p id="stageDetail" class="mono">Click a stage.</p>
<noscript><p>Pipeline, flat order: Open → Claimed → Due within 48h → Expired unclaimed.</p></noscript>
<p><button id="summaryBtn">Post end-of-day summary</button></p>
<pre id="summary"></pre></div>
<aside class="panel"><h2 style="font-size:16px">Claimed tasks</h2><div id="rail">No claims yet today — react ✅ on a digest item to claim it.</div></aside>
</div><script>
async function load(){const d=await (await fetch('/api/digest')).json();
document.getElementById('digest').textContent=d.text;
const box=document.getElementById('items');box.innerHTML='';
d.items.forEach(it=>{const b=document.createElement('button');b.textContent='✅ Claim: '+it.title;
b.onclick=async()=>{b.disabled=true;const r=await (await fetch('/api/claim',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({user_id:'teammate-1',opportunity_id:it.id})})).json();alert(r.reply);b.disabled=false;loadTasks();loadPipeline();};
box.appendChild(b);box.appendChild(document.createElement('br'));box.appendChild(document.createElement('br'));});
loadTasks();loadPipeline();}
async function loadPipeline(){const p=await (await fetch('/api/pipeline')).json();
const labels={open:'Open — waiting for a ✅',claimed:'Claimed — owned',due_within_48h:'Due within 48h — ping these owners',expired_unclaimed:'Expired unclaimed — closed'};
const box=document.getElementById('pipeline');box.innerHTML='';
p.stages.forEach(s=>{const d=document.createElement('div');d.className='stage';d.tabIndex=0;d.setAttribute('role','button');
d.innerHTML=`<b>${p[s]}</b><br>${labels[s]}`;
const show=()=>{document.getElementById('stageDetail').textContent=`${labels[s]}: ${p[s]} item(s) right now.`;};
d.onclick=show;d.onkeydown=e=>{if(e.key==='Enter'||e.key===' '){show();}};
box.appendChild(d);});}
async function loadTasks(){const t=await (await fetch('/api/tasks')).json();
document.getElementById('rail').textContent=t.length?t.map(c=>`✅ ${c.title} — ${c.owner} (due ${c.deadline})`).join('\\n'):'No claims yet today — react ✅ on a digest item to claim it.';}
document.getElementById('summaryBtn').onclick=async()=>{const s=await (await fetch('/api/summary')).json();document.getElementById('summary').textContent=s.text;};
load();
</script></body></html>
"""


class Handler(BaseHTTPRequestHandler):
    store: ClaimStore = make_store()  # replaced per-server in serve()

    def log_message(self, *args):  # keep test output clean
        pass

    def _json(self, obj, status=200):
        body = json.dumps(obj).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self):
        length = int(self.headers.get("Content-Length") or 0)
        if not length:
            return {}
        return json.loads(self.rfile.read(length) or b"{}")

    def do_GET(self):
        path = urlparse(self.path).path
        now = datetime.now(timezone.utc)
        if path == "/":
            body = PAGE.encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        if path == "/api/digest":
            opps = self.store._opportunities.values()  # demo store only
            self._json({
                "text": format_digest(list(opps), now),
                "items": [
                    {"id": o.id, "title": o.title,
                     "deadline": o.deadline.isoformat(),
                     "prize": o.prize, "fit_note": o.fit_note}
                    for o in sorted(opps, key=lambda o: (o.deadline, o.id))
                ],
            })
            return
        if path == "/api/tasks":
            self._json([card_json(c) for c in self.store.task_cards()])
            return
        if path == "/api/pipeline":
            self._json(pipeline_counts(self.store, now))
            return
        if path == "/api/summary":
            self._json({"text": self.store.end_of_day_summary(now)})
            return
        self._json({"error": "not found"}, 404)

    def do_POST(self):
        path = urlparse(self.path).path
        now = datetime.now(timezone.utc)
        try:
            data = self._read_json()
        except Exception:
            self._json({"error": "invalid JSON"}, 400)
            return
        if path == "/api/claim":
            result = self.store.claim(
                str(data.get("user_id", "")), str(data.get("opportunity_id", "")), now
            )
            from digest_room.claims import format_claim_confirmation

            self._json({
                "status": result.status,
                "reply": format_claim_confirmation(result, now),
                "card": card_json(result.card) if result.card else None,
            })
            return
        if path == "/switch/event":
            result = handle_room_event(self.store, data, now)
            self._json({
                "handled": result.handled,
                "claim_status": result.claim_status,
                "reply": result.reply_text,
            })
            return
        self._json({"error": "not found"}, 404)


def serve(port: int | None = None):
    import os

    port = port or int(os.environ.get("PORT", "8000"))
    server = ThreadingHTTPServer(("0.0.0.0", port), Handler)
    print(f"Digest Room harness at http://127.0.0.1:{server.server_address[1]}/")
    print("LOCAL ONLY — not a Switch room. See switch/SWITCH_SETUP.md for the real room.")
    server.serve_forever()


if __name__ == "__main__":
    # No argument so $PORT (set by Render) wins, falling back to 8000 locally.
    # Previously serve(8000) ignored $PORT, which would break Render health checks.
    serve()
