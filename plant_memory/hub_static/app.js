/* PlantMemory Hub — front-end logic (vanilla JS) */
const API = (p, opt) => fetch(p, opt).then(r => r.json());
const el = (h) => { const t = document.createElement('template'); t.innerHTML = h.trim(); return t.content.firstChild; };
const esc = (s) => (s ?? '').toString().replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

const state = { view: 'overview', scenario: '', overview: null, scenarios: [] };
const TITLES = {
  overview: ['Overview', "The plant's living memory at a glance"],
  drift: ['Drift Explorer', 'Simulate a plant change and watch which knowledge is flagged'],
  moc: ['Management of Change', 'Assess and authorise a change by the knowledge it affects'],
  knowledge: ['Knowledge', 'Every diagnostic conclusion, grounded to plant assets'],
  graph: ['Plant Graph', 'Grounded knowledge over the plant topology'],
  inbox: ['Inbox', 'Review proposed additions and corrections'],
  relays: ['Relays', 'Shift handoffs and onboarding batons'],
  evaluation: ['Evaluation', 'Knowledge retention and the cost of change'],
};
const SCEN_VIEWS = new Set(['drift', 'graph', 'moc']);

function toast(msg) {
  const t = document.getElementById('toast');
  t.textContent = msg; t.hidden = false;
  clearTimeout(t._t); t._t = setTimeout(() => t.hidden = true, 2600);
}
function badge(h) {
  const m = { intact: 'b-intact', review: 'b-review', broken: 'b-broken' };
  const lbl = { intact: 'intact', review: 'review', broken: 'broken' };
  return `<span class="badge ${m[h] || 'b-intact'}"><span class="dot"></span>${lbl[h] || h}</span>`;
}

/* ---------- routing ---------- */
document.getElementById('nav').addEventListener('click', e => {
  const b = e.target.closest('.nav-item'); if (!b) return;
  document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
  b.classList.add('active');
  go(b.dataset.view);
});
function go(view) {
  state.view = view;
  const [t, s] = TITLES[view];
  document.getElementById('view-title').textContent = t;
  document.getElementById('view-sub').textContent = s;
  document.getElementById('scenario-box').hidden = !SCEN_VIEWS.has(view);
  render();
}
const scenSel = document.getElementById('scenario-select');
scenSel.addEventListener('change', () => { state.scenario = scenSel.value; render(); });

/* ---------- boot ---------- */
async function boot() {
  state.overview = await API('/api/overview');
  state.scenarios = state.overview.scenarios;
  scenSel.innerHTML = `<option value="">— none (current plant state) —</option>` +
    state.scenarios.map(s => `<option value="${s.name}">${esc(s.description)}</option>`).join('');
  updatePills();
  go('overview');
}
function updatePills() {
  const pi = document.getElementById('pill-inbox'), pr = document.getElementById('pill-relays');
  const pm = document.getElementById('pill-moc');
  const np = state.overview.pending_proposals, nr = state.overview.open_relays;
  const nm = state.overview.open_moc || 0;
  pi.textContent = np; pi.classList.toggle('show', np > 0);
  pr.textContent = nr; pr.classList.toggle('show', nr > 0);
  if (pm) { pm.textContent = nm; pm.classList.toggle('show', nm > 0); }
}
const mocObjBadge = o => `<span class="moc-obj ${o === 'organisational' ? 'org' : 'mat'}">${o === 'organisational' ? 'organisational' : 'material'}</span>`;

/* ---------- render dispatch ---------- */
const view = document.getElementById('view');
function render() {
  const fn = { overview: renderOverview, drift: renderDrift, moc: renderMOC, knowledge: renderKnowledge,
    graph: renderGraph, inbox: renderInbox, relays: renderRelays, evaluation: renderEvaluation }[state.view];
  view.innerHTML = `<div class="empty"><span class="spinner"></span> loading…</div>`;
  fn();
}

/* ---------- Overview ---------- */
async function renderOverview() {
  const o = state.overview = await API('/api/overview?scenario=' + encodeURIComponent(state.scenario));
  updatePills();
  const bh = o.health || o.base_health;
  const active = !!o.scenario;
  const pct = (bh.retained_fraction * 100) | 0;
  const healthLbl = active ? 'retained under this change' : 'healthy vs current state';
  const flaggedTxt = bh.flagged > 0
    ? `<b style="color:var(--review)">${bh.flagged} flagged</b>`
    : '0 flagged';
  const cats = Object.entries(o.categories).map(([k, v]) =>
    `<div class="meta"><span class="cat">${esc(k)}</span><span class="tag">${v}</span></div>`).join('');
  view.innerHTML = `
    <div class="hero-note">PlantMemory keeps every diagnosis <b>grounded</b> to the sensors and equipment it relied on.
      When the plant changes, only the knowledge tied to what changed is flagged — the rest is retained.
      <b>No relearning from scratch.</b></div>
    <div class="grid cols-4">
      <div class="card stat"><div class="val accent">${o.corpus_size}</div><div class="lbl">knowledge entries</div><div class="sub">grounded &amp; versioned</div></div>
      <div class="card stat"><div class="val"${active && pct < 100 ? ' style="color:var(--review)"' : ''}>${pct}%</div><div class="lbl">${healthLbl}</div><div class="sub">${bh.intact} intact · ${flaggedTxt}</div></div>
      <div class="card stat"><div class="val">${o.pending_proposals}</div><div class="lbl">pending proposals</div><div class="sub">awaiting review</div></div>
      <div class="card stat"><div class="val">${o.open_relays}</div><div class="lbl">open relays</div><div class="sub">handoffs in flight</div></div>
    </div>
    <div class="section-title">Simulate a plant change</div>
    <div class="grid cols-3" id="scen-grid">
      ${o.scenarios.map(s => `<div class="scenario-card" data-scen="${s.name}">
        <div class="sk">${esc(s.kind)} ${mocObjBadge(s.moc_object)}</div><div class="st">${esc(niceName(s.name))}</div>
        <div class="sd">${esc(s.description)}</div></div>`).join('')}
    </div>
    <div class="section-title">Knowledge by category</div>
    <div class="card"><div class="meta" style="gap:14px">${cats}</div></div>`;
  view.querySelectorAll('.scenario-card').forEach(c => c.onclick = () => {
    state.scenario = c.dataset.scen; scenSel.value = c.dataset.scen;
    document.querySelector('.nav-item[data-view="drift"]').click();
  });
}
const niceName = n => n.replace(/_/g, ' ').replace(/\b\w/g, m => m.toUpperCase());

/* ---------- Drift Explorer ---------- */
async function renderDrift() {
  const d = await API('/api/knowledge?scenario=' + encodeURIComponent(state.scenario));
  const s = await API('/api/drift?scenario=' + encodeURIComponent(state.scenario));
  const sm = s.summary;
  const pct = Math.round(sm.retained_fraction * 100);
  const scDesc = state.scenario ? state.scenarios.find(x => x.name === state.scenario)?.description : 'No change applied — every entry should be intact.';
  view.innerHTML = `
    <div class="grid cols-2" style="grid-template-columns:340px 1fr;align-items:stretch">
      <div class="card">
        <h3>Knowledge health</h3>
        <div class="gauge-wrap">
          <div class="gauge" style="--p:${pct}"><div><div class="g-num">${pct}%</div><div class="g-lbl">retained</div></div></div>
          <div>
            <div class="stat" style="margin-bottom:10px"><div class="val" style="font-size:22px">${sm.intact}/${sm.total}</div><div class="lbl">entries intact</div></div>
            <div>${badge('review')} <b>${sm.review}</b> need review</div>
            <div style="margin-top:6px">${badge('broken')} <b>${sm.broken}</b> broken</div>
          </div>
        </div>
        <p class="muted" style="margin:16px 0 0;font-size:12.5px">${esc(scDesc)}</p>
      </div>
      <div class="card">
        <h3>What this means</h3>
        <p class="muted" style="font-size:13.5px">A <b style="color:var(--review)">review</b> flag means the plant condition a piece of knowledge relied on has moved — an engineer should re-confirm it, not discard it. A <b style="color:var(--broken)">broken</b> flag means an asset it depended on is gone.</p>
        <p class="muted" style="font-size:13.5px">Under this change, <b style="color:var(--ink)">${sm.flagged} of ${sm.total}</b> entries are flagged. The other <b style="color:var(--ink)">${sm.intact}</b> carry over untouched — that is the knowledge you would have thrown away by retraining from scratch.</p>
        ${state.scenario ? `<button class="btn sm" id="mk-relay">Create a handoff for this change →</button>` : ''}
      </div>
    </div>
    <div class="section-title">Knowledge entries ${state.scenario ? 'after this change' : ''}</div>
    <div class="klist">${d.entries.map(kcard).join('')}</div>`;
  wireKcards();
  const mk = document.getElementById('mk-relay');
  if (mk) mk.onclick = async () => {
    await API('/api/relays', { method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title: 'Handoff: ' + niceName(state.scenario), by: 'engineer', to: 'team', scenario: state.scenario,
        summary: 'Auto-generated from drift under ' + state.scenario }) });
    toast('Relay created with the flagged items as a watch-list'); boot();
  };
}
function kcard(e) {
  const reasons = (e.reasons || []).slice(0, 4).map(r =>
    `<div class="reason ${e.health === 'broken' ? 'br' : ''}">${esc(r)}</div>`).join('');
  return `<div class="kcard h-${e.health}" data-id="${e.id}">
    <div class="top"><div><div class="title">${esc(e.title)}</div><div class="stmt">${esc(e.statement)}</div></div>${badge(e.health)}</div>
    <div class="meta"><span class="cat">${esc(e.category)}</span>${(e.tags_referenced||[]).slice(0,5).map(t=>`<span class="tag">${esc(t)}</span>`).join('')}
      <span class="dim" style="margin-left:auto;font-size:12px">conf ${e.live_confidence?.toFixed?.(2) ?? e.confidence}</span></div>
    ${reasons ? `<div class="reasons">${reasons}</div>` : ''}</div>`;
}
function wireKcards() {
  view.querySelectorAll('.kcard').forEach(c => c.onclick = () => openEntry(c.dataset.id));
}

/* ---------- Knowledge ---------- */
let _kAll = [], _kFilter = '', _kCat = '';
async function renderKnowledge() {
  const d = await API('/api/knowledge?scenario=' + encodeURIComponent(state.scenario));
  _kAll = d.entries;
  const cats = [...new Set(_kAll.map(e => e.category))];
  view.innerHTML = `
    <div class="toolbar">
      <input class="search" id="ksearch" placeholder="Search knowledge, tags, causes…">
      <span class="chip ${_kCat===''?'active':''}" data-cat="">all</span>
      ${cats.map(c => `<span class="chip ${_kCat===c?'active':''}" data-cat="${c}">${esc(c)}</span>`).join('')}
    </div>
    <div class="klist" id="klist"></div>`;
  const draw = () => {
    const q = _kFilter.toLowerCase();
    const items = _kAll.filter(e => (!_kCat || e.category === _kCat) &&
      (!q || (e.title + e.statement + (e.tags_referenced||[]).join(' ')).toLowerCase().includes(q)));
    document.getElementById('klist').innerHTML = items.length ? items.map(kcard).join('') : `<div class="empty">no matches</div>`;
    wireKcards();
  };
  const si = document.getElementById('ksearch');
  si.oninput = () => { _kFilter = si.value; draw(); };
  view.querySelectorAll('.chip').forEach(ch => ch.onclick = () => { _kCat = ch.dataset.cat;
    view.querySelectorAll('.chip').forEach(x => x.classList.remove('active')); ch.classList.add('active'); draw(); });
  draw();
}

/* ---------- entry drawer ---------- */
async function openEntry(id) {
  const e = await API('/api/knowledge/' + id + '?scenario=' + encodeURIComponent(state.scenario));
  const dr = e.drift || { groundings: [], health: 'intact' };
  const gr = dr.groundings.map(g => {
    const st = g.status; const cls = st === 'changed' ? 'changed' : st === 'missing' ? 'missing' : '';
    const col = st === 'changed' ? 'var(--review)' : st === 'missing' ? 'var(--broken)' : 'var(--intact)';
    return `<div class="ground-row ${cls}">
      <div><span class="gk">${esc(g.grounding.kind)}:${esc(g.grounding.ref)}</span> <span class="dim">· ${esc(g.grounding.aspect)}</span>
        ${g.detail ? `<div class="muted" style="font-size:12px;margin-top:4px">${esc(g.detail)}</div>` : ''}</div>
      <div class="status-tag" style="color:${col}">${esc(st)}</div></div>`;
  }).join('');
  const panel = document.getElementById('drawer-panel');
  panel.innerHTML = `
    <div style="display:flex;justify-content:space-between;align-items:center">
      <span class="cat">${esc(e.category)} · ${esc(e.id)}</span>
      <button class="btn ghost sm" data-close>Close</button></div>
    <h2 style="margin:12px 0 6px;font-size:20px">${esc(e.title)}</h2>
    <div style="margin-bottom:14px">${badge(dr.health)} <span class="dim" style="font-size:12px">confidence ${dr.confidence ?? e.confidence}</span></div>
    <p style="font-size:14.5px">${esc(e.statement)}</p>
    ${e.body ? `<p class="muted" style="white-space:pre-wrap;font-size:13px">${esc(e.body)}</p>` : ''}
    ${e.corrective_actions?.length ? `<h3 style="margin:18px 0 8px;font-size:13px;color:var(--muted);text-transform:uppercase;letter-spacing:.6px">Corrective actions</h3>
      <ol style="margin:0;padding-left:20px;font-size:13.5px">${e.corrective_actions.map(a=>`<li style="margin-bottom:5px">${esc(a)}</li>`).join('')}</ol>` : ''}
    <h3 style="margin:20px 0 8px;font-size:13px;color:var(--muted);text-transform:uppercase;letter-spacing:.6px">Grounded to (${dr.groundings.length})</h3>
    ${gr}
    ${e.evidence?.length ? `<h3 style="margin:18px 0 8px;font-size:13px;color:var(--muted);text-transform:uppercase;letter-spacing:.6px">Evidence</h3>
      <div class="muted" style="font-size:12.5px">${e.evidence.map(esc).join(' · ')}</div>` : ''}`;
  const drawer = document.getElementById('drawer');
  drawer.hidden = false;
  drawer.querySelectorAll('[data-close]').forEach(x => x.onclick = () => drawer.hidden = true);
}

/* ---------- Plant Graph ---------- */
async function renderGraph() {
  const g = await API('/api/graph?scenario=' + encodeURIComponent(state.scenario));
  const W = 1180, H = 560, padX = 90, padY = 46;
  const nCols = g.columns.length;
  const colW = (W - padX * 2) / (nCols - 1);
  const pos = {};
  g.nodes.forEach(n => {
    const x = padX + n.col * colW;
    const y = padY + (n.n_rows === 1 ? (H - padY * 2) / 2 : (n.row) * (H - padY * 2) / Math.max(n.n_rows - 1, 1));
    pos[n.id] = { x, y, n };
  });
  const edgeLines = g.edges.map(e => {
    const a = pos[e.source], b = pos[e.target]; if (!a || !b) return '';
    const chg = a.n.changed || b.n.changed || a.n.missing || b.n.missing;
    return `<line x1="${a.x}" y1="${a.y}" x2="${b.x}" y2="${b.y}" stroke="${chg ? 'rgba(245,166,35,.5)' : 'rgba(120,140,160,.16)'}" stroke-width="${chg ? 1.6 : 1}"/>`;
  }).join('');
  const nodeMarks = g.nodes.map(n => {
    const p = pos[n.id];
    let fill = '#33465a', stroke = '#4a6076', r = n.type === 'Sensor' ? 5 : 7;
    if (n.grounded) { fill = '#1c6f5c'; stroke = 'var(--intact)'; }
    if (n.changed) { fill = '#7a5410'; stroke = 'var(--review)'; r += 2; }
    if (n.missing) { fill = '#7a2320'; stroke = 'var(--broken)'; r += 2; }
    const label = ['System', 'Equipment', 'Boundary', 'Plant', 'ControlLoop'].includes(n.type)
      ? `<text x="${p.x + 10}" y="${p.y + 4}" font-size="10.5" fill="#9db2c4">${esc(shorten(n.name))}</text>` : '';
    const cls = n.changed ? 'gnode pulse' : 'gnode';
    return `<g class="${cls}"><circle cx="${p.x}" cy="${p.y}" r="${r}" fill="${fill}" stroke="${stroke}" stroke-width="1.6">
      <title>${esc(n.name)} [${esc(n.type)}]${n.grounded ? ' · grounded' : ''}${n.changed ? ' · CHANGED' : ''}${n.missing ? ' · MISSING' : ''}</title></circle>${label}</g>`;
  }).join('');
  const colHeaders = g.columns.map((c, i) =>
    `<text x="${padX + i * colW}" y="24" font-size="11" fill="#5f7285" text-anchor="middle" letter-spacing="1">${c.toUpperCase()}</text>`).join('');
  view.innerHTML = `
    <div class="graph-wrap">
      <svg viewBox="0 0 ${W} ${H}" width="100%" preserveAspectRatio="xMidYMid meet">
        ${colHeaders}${edgeLines}${nodeMarks}
      </svg>
    </div>
    <div class="legend">
      <span><i style="background:#33465a"></i> plant asset</span>
      <span><i style="background:#1c6f5c;outline:1px solid var(--intact)"></i> grounded by knowledge</span>
      <span><i style="background:#7a5410;outline:1px solid var(--review)"></i> changed under scenario</span>
      <span><i style="background:#7a2320;outline:1px solid var(--broken)"></i> removed</span>
    </div>
    <p class="muted" style="font-size:13px;margin-top:12px">${g.changed_nodes.length || g.changed_tags.length
      ? `This change touches <b style="color:var(--review)">${[...g.changed_nodes, ...g.changed_tags].length}</b> grounded assets. Knowledge anchored to them is flagged for review.`
      : 'Select a plant change above to see which grounded assets it disturbs.'}</p>`;
}
const shorten = s => s.length > 26 ? s.slice(0, 24) + '…' : s;

/* ---------- Inbox ---------- */
async function renderInbox() {
  const d = await API('/api/inbox');
  const props = d.proposals;
  if (!props.length) { view.innerHTML = `<div class="empty">No proposals yet. Agents draft additions/corrections here for your review.</div>`; return; }
  view.innerHTML = props.map(p => {
    const e = p.entry;
    const pend = p.status === 'pending';
    return `<div class="prop" data-id="${p.proposal_id}">
      <div class="ph"><div><b>${esc(e.title)}</b> <span class="dim">· ${esc(p.kind)}</span></div>
        <span class="status-${p.status}">${esc(p.status)}</span></div>
      <p class="muted" style="font-size:13.5px;margin:8px 0">${esc(e.statement)}</p>
      <div class="meta"><span class="dim" style="font-size:12px">by ${esc(p.proposer)}</span>
        ${(e.tags_referenced||[]).slice(0,6).map(t=>`<span class="tag">${esc(t)}</span>`).join('')}</div>
      ${p.rationale ? `<p class="muted" style="font-size:12.5px;margin-top:8px">Rationale: ${esc(p.rationale)}</p>` : ''}
      ${pend ? `<div class="actions"><button class="btn sm" data-approve>Approve into memory</button>
        <button class="btn ghost sm" data-reject>Reject</button></div>` :
        `<div class="muted" style="font-size:12px;margin-top:10px">decided by ${esc(p.decided_by||'—')} ${p.approved_entry_id ? '→ '+esc(p.approved_entry_id):''}</div>`}
    </div>`;
  }).join('');
  view.querySelectorAll('.prop').forEach(pc => {
    const id = pc.dataset.id;
    pc.querySelector('[data-approve]')?.addEventListener('click', async () => {
      const r = await API(`/api/inbox/${id}/approve`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ by: 'reviewer' }) });
      toast('Approved → ' + (r.entry_id || 'added to memory')); await boot(); go('inbox');
    });
    pc.querySelector('[data-reject]')?.addEventListener('click', async () => {
      await API(`/api/inbox/${id}/reject`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ by: 'reviewer' }) });
      toast('Rejected'); await boot(); go('inbox');
    });
  });
}

/* ---------- Relays ---------- */
async function renderRelays() {
  const d = await API('/api/relays');
  const scenOpts = state.scenarios.map(s => `<option value="${s.name}">${esc(niceName(s.name))}</option>`).join('');
  view.innerHTML = `
    <div class="grid cols-2" style="grid-template-columns:1fr 360px;align-items:start">
      <div>
        <div class="section-title" style="margin-top:0">Handoffs</div>
        <div id="relaylist">${d.relays.length ? d.relays.slice().reverse().map(relayCard).join('') : `<div class="empty">No relays yet.</div>`}</div>
      </div>
      <div class="card">
        <h3>Create a handoff</h3>
        <div class="form">
          <label>Title</label><input id="r-title" value="Shift handoff">
          <label>From</label><input id="r-by" value="engineer">
          <label>Summary</label><textarea id="r-sum" rows="3" placeholder="What the next person needs to know…"></textarea>
          <label>Attach knowledge health under change (optional)</label>
          <select id="r-scen"><option value="">current state</option>${scenOpts}</select>
          <button class="btn" id="r-create">Create relay</button>
        </div>
      </div>
    </div>`;
  document.getElementById('r-create').onclick = async () => {
    const body = { title: v('r-title'), by: v('r-by'), summary: v('r-sum'), scenario: v('r-scen') || null, to: 'team' };
    await API('/api/relays', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
    toast('Relay created'); await boot(); go('relays');
  };
  wireRelays();
}
const v = id => document.getElementById(id).value;
function relayCard(r) {
  const c = r.context || {};
  return `<div class="prop" data-id="${r.relay_id}">
    <div class="ph"><div><b>${esc(r.title)}</b> <span class="dim">· ${esc(r.relay_id)}</span></div><span class="status-${r.status}">${esc(r.status)}</span></div>
    <p class="muted" style="font-size:13.5px;margin:8px 0">${esc(r.summary || '')}</p>
    <div class="meta"><span class="dim" style="font-size:12px">from ${esc(r.from_member)} → ${esc(r.to)}</span>
      ${c.flagged_count ? `<span class="badge b-review"><span class="dot"></span>${c.flagged_count} to watch</span>` : ''}
      ${(c.watch_tags||[]).slice(0,6).map(t=>`<span class="tag">${esc(t)}</span>`).join('')}</div>
    ${(c.flagged||[]).length ? `<div class="reasons">${c.flagged.slice(0,3).map(f=>`<div class="reason">${esc(f.title)}</div>`).join('')}</div>` : ''}
    <div class="actions">
      ${r.status==='open'?`<button class="btn sm" data-take>Take baton</button>`:''}
      ${r.status!=='closed'?`<button class="btn ghost sm" data-close2>Close</button>`:''}
      <span class="dim" style="font-size:11.5px;margin-left:auto;align-self:center">${r.observed_state? 'branch '+esc(r.observed_state.branch||'—'):''}</span>
    </div></div>`;
}
function wireRelays() {
  view.querySelectorAll('.prop').forEach(pc => {
    const id = pc.dataset.id;
    pc.querySelector('[data-take]')?.addEventListener('click', async () => {
      await API(`/api/relays/${id}/take`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ by: 'Sam' }) });
      toast('Baton taken'); await boot(); go('relays');
    });
    pc.querySelector('[data-close2]')?.addEventListener('click', async () => {
      await API(`/api/relays/${id}/close`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ by: 'Sam' }) });
      toast('Relay closed'); await boot(); go('relays');
    });
  });
}

/* ---------- Management of Change (MOC) ---------- */
async function renderMOC() {
  const scen = state.scenario;
  const a = await API('/api/moc/assess?scenario=' + encodeURIComponent(scen));
  const reg = await API('/api/moc');
  const intro = `<div class="hero-note">Every change in a plant must pass <b>Management of Change</b>: describe the change, assess its impact, and authorise it before it takes effect. Conventional MOC is manual and conservative. PlantMemory makes the <b>impact assessment automatic</b> — it shows exactly which knowledge a change invalidates — and keeps an auditable approval record.</div>`;

  let requestHtml;
  if (!scen) {
    requestHtml = `<div class="card"><h3>Raise a change request</h3>
      <p class="muted" style="font-size:13.5px">Pick a change from the <b>Simulate plant change</b> selector above. PlantMemory classifies it as <span class="moc-obj mat">material</span> or <span class="moc-obj org">organisational</span>, then assesses which knowledge it affects before you authorise it.</p></div>`;
  } else {
    const rec = a.recommendation || {};
    const rows = (a.impacted || []).map(x => `
      <div class="reason" style="display:flex;justify-content:space-between;gap:10px;align-items:center">
        <span>${badge(x.health)} ${esc(x.title)}</span>
        <span class="dim" style="font-size:12px;white-space:nowrap">conf ${x.confidence_before ?? '—'} → <b style="color:var(--review)">${x.confidence_after ?? '—'}</b></span>
      </div>`).join('');
    requestHtml = `
      <div class="card">
        <div class="ph"><div><b>Change request</b> <span class="dim">· ${esc(niceName(scen))}</span></div>${mocObjBadge(a.moc_object)}</div>
        <p class="muted" style="font-size:13.5px;margin:8px 0">${esc(a.description)}</p>
        <div class="meta"><span class="tag">${esc(a.moc_class)}</span><span class="tag">${esc(a.kind)}</span></div>
        <div class="section-title" style="margin:16px 0 8px">Automatic impact assessment</div>
        <div class="grid cols-4" style="gap:10px">
          <div class="card stat"><div class="val">${a.impacted_count}</div><div class="lbl">knowledge affected</div></div>
          <div class="card stat"><div class="val" style="color:var(--review)">${a.n_review}</div><div class="lbl">need review</div></div>
          <div class="card stat"><div class="val" style="color:var(--broken)">${a.n_broken}</div><div class="lbl">broken</div></div>
          <div class="card stat"><div class="val accent">${a.unaffected}</div><div class="lbl">unaffected, kept</div></div>
        </div>
        ${rows ? `<div class="reasons" style="margin-top:12px">${rows}</div>` : `<p class="muted" style="font-size:13px;margin-top:10px">No encoded knowledge depends on what this change touches.</p>`}
        <div class="assess-rec rec-${esc(rec.level)}">${esc(rec.text || '')}</div>
        <div class="actions"><button class="btn" id="moc-raise">Raise MOC record →</button></div>
      </div>`;
  }

  const recCards = (reg.records || []).map(mocCard).join('');
  view.innerHTML = intro + requestHtml +
    `<div class="section-title">MOC register</div>
     <div id="moclist">${recCards || `<div class="empty">No change records yet. Raise one from a selected change above.</div>`}</div>`;

  const raise = document.getElementById('moc-raise');
  if (raise) raise.onclick = async () => {
    await API('/api/moc/raise', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ scenario: scen, by: 'engineer' }) });
    toast('MOC record raised'); await boot(); go('moc');
  };
  wireMOC();
}
function mocCard(r) {
  const a = r.assessment || {};
  return `<div class="prop" data-id="${r.moc_id}">
    <div class="ph"><div><b>${esc(r.title)}</b> <span class="dim">· ${esc(r.moc_id)}</span></div><span class="status-${r.status}">${esc(r.status)}</span></div>
    <div class="meta" style="margin:8px 0">${mocObjBadge(r.moc_object)}<span class="tag">${esc(r.moc_class)}</span>
      ${a.impacted_count ? `<span class="badge b-review"><span class="dot"></span>${a.impacted_count} affected</span>` : `<span class="badge b-intact"><span class="dot"></span>no impact</span>`}
      ${r.decided_by ? `<span class="dim" style="font-size:12px">by ${esc(r.decided_by)}</span>` : ''}</div>
    <div class="actions">
      ${r.status === 'open' ? `<button class="btn sm" data-approve>Approve change</button><button class="btn ghost sm" data-reject>Reject</button>` : ''}
    </div></div>`;
}
function wireMOC() {
  view.querySelectorAll('.prop').forEach(pc => {
    const id = pc.dataset.id;
    pc.querySelector('[data-approve]')?.addEventListener('click', async () => {
      await API(`/api/moc/${id}/approve`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ by: 'approver' }) });
      toast('Change authorised'); await boot(); go('moc');
    });
    pc.querySelector('[data-reject]')?.addEventListener('click', async () => {
      await API(`/api/moc/${id}/reject`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ by: 'approver' }) });
      toast('Change rejected'); await boot(); go('moc');
    });
  });
}

/* ---------- Evaluation ---------- */
async function renderEvaluation() {
  view.innerHTML = `<div class="empty"><span class="spinner"></span> running evaluation across all change scenarios…</div>`;
  const r = await API('/api/evaluate');
  const c = r.cost_model;
  const bust = '?t=' + Date.now();
  view.innerHTML = `
    <div class="grid cols-3">
      <div class="card stat"><div class="val accent">${Math.round(c.savings_fraction*100)}%</div><div class="lbl">re-validation effort saved</div><div class="sub">vs relearning from scratch</div></div>
      <div class="card stat"><div class="val">${c.targeted_revalidation_cost} <span class="dim" style="font-size:16px">/ ${c.relearn_from_scratch_cost}</span></div><div class="lbl">items re-validated (targeted / naive)</div><div class="sub">${c.scenarios} plant changes</div></div>
      <div class="card stat"><div class="val">${Math.round(c.avg_retained_fraction*100)}%</div><div class="lbl">avg knowledge retained</div><div class="sub">per change</div></div>
    </div>
    <div class="section-title">Cost of absorbing change</div>
    <div class="grid cols-2">
      <div class="card"><img class="plot" src="/plots/cost_comparison.png${bust}"></div>
      <div class="card"><img class="plot" src="/plots/retention_by_scenario.png${bust}"></div>
    </div>
    <div class="section-title">Which knowledge drifts under which change</div>
    <div class="card"><img class="plot" src="/plots/drift_matrix.png${bust}"></div>
    <p class="muted" style="font-size:13px;margin-top:14px">Each column is a real plant change; each row a piece of knowledge.
      Mostly green means the corpus survives change — knowledge is invalidated <b>surgically</b>, not wholesale.</p>`;
}

document.getElementById('drawer').addEventListener('click', e => { if (e.target.classList.contains('drawer-scrim')) document.getElementById('drawer').hidden = true; });
boot();
