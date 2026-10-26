/* Full map: every topic and prerequisite link, filterable by level, with ancestor/descendant highlighting. */
(function () {
  'use strict';
  const h = QM.h;
  const LS_KEY = 'qmMap.levels.v1';
  let D, byId, cy = null, selected = null;
  const params = new URLSearchParams(location.search);

  if (window.cytoscapeDagre) window.cytoscape.use(window.cytoscapeDagre);

  QM.loadData('../').then(init).catch(function (e) {
    document.getElementById('summary').textContent = 'Could not load data: ' + e.message;
  });

  function init(data) {
    D = data;
    byId = {};
    D.topics.forEach(function (t) { byId[t.id] = t; });

    // levels in teaching order: Year 9, Year 10, Year 10 Optional, then each senior unit
    const vols = [];
    const count = {};
    D.topics.forEach(function (t) {
      const v = QM.volumeOf(t);
      if (!count[v]) { count[v] = 0; vols.push({ v: v, band: t.band }); }
      count[v]++;
    });
    const rank = function (x) { return E_rank(byId[D.topics.find(function (t) { return QM.volumeOf(t) === x.v; }).id]); };
    vols.sort(function (a, b) { return rank(a) - rank(b); });

    let saved = null;
    try { saved = JSON.parse(localStorage.getItem(LS_KEY)); } catch (e) { /* ignore */ }
    const fromUrl = params.get('levels');
    const on = new Set(fromUrl ? fromUrl.split(',') : (Array.isArray(saved) ? saved : vols.map(function (x) { return x.v; })));

    const box = document.getElementById('levels');
    vols.forEach(function (x) {
      const c = QM.bandColors(x.band);
      const cb = h('input', { type: 'checkbox', value: x.v, checked: on.has(x.v) || null, onchange: redraw });
      box.append(h('label', null, cb, h('span', { class: 'swatch', style: 'background:' + c.bg + ';border-color:' + c.fg }),
        QM.volumeLabel(x.v), h('span', { class: 'n', text: String(count[x.v]) })));
    });
    document.getElementById('all').onclick = function () { setAll(true); };
    document.getElementById('none').onclick = function () { setAll(false); };
    document.getElementById('soft').onchange = redraw;
    document.getElementById('fit').onclick = function () { if (cy) cy.fit(cy.elements(':visible'), 30); };
    document.getElementById('zin').onclick = function () { zoom(1.25); };
    document.getElementById('zout').onclick = function () { zoom(0.8); };
    document.getElementById('q').addEventListener('input', search);
    redraw();
    if (params.get('focus') && byId[params.get('focus')]) select(params.get('focus'));
  }

  // same ordering as engine.gradeRank: Year 9 < Year 10 < optional < U1 ... U4
  function E_rank(t) {
    if (t.band === 'y9') return 0;
    if (t.band === 'y10') return 1;
    if (t.band === 'y10opt') return 2;
    return 2 + (t.unit || 0) + (t.band === 'general' ? 0.1 : t.band === 'specialist' ? 0.2 : 0);
  }

  function setAll(v) {
    document.querySelectorAll('#levels input').forEach(function (cb) { cb.checked = v; });
    redraw();
  }

  function zoom(f) {
    if (!cy) return;
    cy.zoom({ level: cy.zoom() * f, renderedPosition: { x: cy.width() / 2, y: cy.height() / 2 } });
  }

  function shownLevels() {
    return new Set(Array.from(document.querySelectorAll('#levels input:checked')).map(function (cb) { return cb.value; }));
  }

  function redraw() {
    const levels = shownLevels();
    try { localStorage.setItem(LS_KEY, JSON.stringify(Array.from(levels))); } catch (e) { /* ignore */ }
    const showSoft = document.getElementById('soft').checked;
    const nodes = D.topics.filter(function (t) { return levels.has(QM.volumeOf(t)); });
    const ids = new Set(nodes.map(function (t) { return t.id; }));
    const edges = D.deps.filter(function (e) {
      return ids.has(e.topicId) && ids.has(e.prerequisiteId) && (showSoft || e.strength === 'hard');
    });
    const hard = edges.filter(function (e) { return e.strength === 'hard'; }).length;
    document.getElementById('summary').textContent = nodes.length + ' of ' + D.topics.length + ' topics · ' +
      edges.length + ' links (' + hard + ' hard, ' + (edges.length - hard) + ' soft)';

    const els = nodes.map(function (t) {
      const c = QM.bandColors(t.band);
      return { data: { id: t.id, label: QM.clip(t.name, 40), fg: c.fg, bg: c.bg } };
    }).concat(edges.map(function (e) {
      return { data: { id: e.prerequisiteId + '>' + e.topicId, source: e.prerequisiteId, target: e.topicId, strength: e.strength } };
    }));

    if (cy) cy.destroy();
    const text = QM.cssVar('--text');
    cy = window.cytoscape({
      container: document.getElementById('cy'), elements: els, minZoom: 0.05, maxZoom: 2.5,
      style: [
        { selector: 'node', style: { shape: 'round-rectangle', 'background-color': 'data(bg)', 'border-color': 'data(fg)', 'border-width': 1.5,
          label: 'data(label)', color: text, 'font-size': 11, 'text-wrap': 'wrap', 'text-max-width': 140, 'text-valign': 'center',
          width: 160, height: 46, 'transition-property': 'opacity', 'transition-duration': '120ms' } },
        { selector: 'edge', style: { width: 1.4, 'line-color': QM.cssVar('--edge'), 'target-arrow-color': QM.cssVar('--edge'),
          'target-arrow-shape': 'triangle', 'arrow-scale': 0.8, 'curve-style': 'bezier', opacity: 0.75 } },
        { selector: 'edge[strength = "soft"]', style: { 'line-style': 'dashed', 'line-color': QM.cssVar('--edge-soft'), 'target-arrow-color': QM.cssVar('--edge-soft') } },
        { selector: '.faded', style: { opacity: 0.12 } },
        { selector: 'node.focus', style: { 'border-width': 5 } },
        { selector: 'node.up', style: { 'border-width': 3 } },
        { selector: 'node.down', style: { 'border-width': 3, 'border-style': 'dashed' } },
        { selector: 'edge.lit', style: { width: 2.6, opacity: 1 } },
        { selector: 'node.match', style: { 'border-width': 5, 'border-color': QM.cssVar('--brand') } }
      ],
      layout: window.cytoscapeDagre ? { name: 'dagre', rankDir: 'TB', nodeSep: 16, rankSep: 56, edgeSep: 8 } : { name: 'breadthfirst', directed: true }
    });
    cy.on('tap', 'node', function (e) { select(e.target.id()); });
    cy.on('tap', function (e) { if (e.target === cy) clearSelection(); });
    cy.on('dbltap', 'node', function (e) { location.href = '../explore/#' + e.target.id(); });
    cy.fit(undefined, 30);
    if (selected && ids.has(selected)) select(selected, true); else clearSelection();
    search();
  }

  function clearSelection() {
    selected = null;
    if (cy) cy.elements().removeClass('faded focus up down lit');
    const box = document.getElementById('sel');
    box.textContent = '';
    box.append(h('p', { class: 'muted small', text: 'Click a topic to highlight everything it depends on (above) and everything that builds on it (below). Double-click to open it. Click empty space to clear.' }));
  }

  function select(id, keepView) {
    if (!cy) return;
    const n = cy.getElementById(id);
    if (!n.length) return;
    selected = id;
    const up = n.predecessors();    // prerequisites, all the way back, with their edges
    const down = n.successors();    // topics that build on it, with their edges
    cy.elements().removeClass('faded focus up down lit').addClass('faded');
    n.removeClass('faded').addClass('focus');
    up.removeClass('faded'); up.nodes().addClass('up'); up.edges().addClass('lit');
    down.removeClass('faded'); down.nodes().addClass('down'); down.edges().addClass('lit');
    if (!keepView) cy.animate({ fit: { eles: n.union(up).union(down), padding: 40 }, duration: 250 });

    const t = byId[id];
    const names = function (col) {
      return col.nodes().map(function (x) { return x.id(); })
        .sort(function (a, b) { return E_rank(byId[a]) - E_rank(byId[b]); });
    };
    const direct = D.deps.filter(function (e) { return e.topicId === id; });
    const box = document.getElementById('sel');
    box.textContent = '';
    box.append(h('div', null, QM.bandTag(t), h('h3', { text: t.name }),
      h('p', { class: 'small muted', text: up.nodes().length + ' topics before it · ' + down.nodes().length + ' build on it' }),
      direct.length ? [h('b', { class: 'small', text: 'Needs directly' }),
        h('ul', null, direct.map(function (e) {
          return h('li', null, h('span', { class: 'tag ' + e.strength, text: e.strength }), ' ',
            h('a', { href: '#', text: byId[e.prerequisiteId].name, onclick: function (ev) { ev.preventDefault(); select(e.prerequisiteId); } }));
        }))] : h('p', { class: 'small muted', text: t.root_reason || 'No prerequisites in this map.' }),
      down.nodes().length ? [h('b', { class: 'small', text: 'Builds towards' }),
        h('ul', null, names(down).slice(0, 8).map(function (x) { return h('li', { text: byId[x].name }); }),
          down.nodes().length > 8 ? h('li', { class: 'muted', text: '…and ' + (down.nodes().length - 8) + ' more' }) : null)] : null,
      h('div', { class: 'row' },
        h('a', { class: 'btn small', href: '../explore/#' + id, text: 'Open in Explore' }),
        h('a', { class: 'btn small primary', href: '../diagnose/?target=' + id, text: 'Diagnose' }))));
  }

  function search() {
    if (!cy) return;
    const q = document.getElementById('q').value.trim().toLowerCase();
    cy.nodes().removeClass('match');
    if (!q) return;
    const hits = cy.nodes().filter(function (n) {
      const t = byId[n.id()];
      return (t.name + ' ' + t.id).toLowerCase().indexOf(q) >= 0;
    });
    hits.addClass('match');
    if (hits.length) cy.animate({ fit: { eles: hits, padding: 80 }, duration: 250 });
  }
})();
