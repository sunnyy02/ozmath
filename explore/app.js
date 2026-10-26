/* Explore: topic list, topic detail and a local prerequisite graph (Cytoscape + dagre). */
(function () {
  'use strict';
  const h = QM.h;
  const TYPE_LABEL = { conceptual: 'Conceptual', procedural: 'Procedural', reasoning: 'Reasoning', application: 'Application', modelling: 'Modelling' };
  const TECH_LABEL = { free: 'Technology-free', active: 'Technology-active', either: 'Either' };
  let D, byId, prereqs, dependents, qByTopic, cy = null;
  let depthUp = 2;
  const params = new URLSearchParams(location.search);

  QM.loadData('../').then(init).catch(function (e) {
    document.getElementById('list').textContent = 'Could not load data: ' + e.message;
  });

  function init(data) {
    D = data;
    byId = {}; prereqs = {}; dependents = {}; qByTopic = {};
    D.topics.forEach(function (t) { byId[t.id] = t; prereqs[t.id] = []; dependents[t.id] = []; qByTopic[t.id] = []; });
    D.deps.forEach(function (d) {
      if (!byId[d.topicId] || !byId[d.prerequisiteId]) return;
      prereqs[d.topicId].push(d);
      dependents[d.prerequisiteId].push(d);
    });
    D.questions.forEach(function (q) { if (qByTopic[q.topicId]) qByTopic[q.topicId].push(q); });
    const sel = document.getElementById('band');
    QM.BANDS.forEach(function (b) {
      if (D.topics.some(function (t) { return t.band === b.id; })) sel.append(h('option', { value: b.id, text: b.label }));
    });
    sel.value = params.get('band') || '';
    sel.addEventListener('change', renderList);
    document.getElementById('q').addEventListener('input', renderList);
    window.addEventListener('hashchange', route);
    renderList();
    route();
  }

  function current() { return decodeURIComponent(location.hash.slice(1)); }

  function route() {
    let id = current();
    const alias = D.aliases[id];
    if (alias) id = (alias.targets || alias)[0];
    if (!byId[id]) id = D.topics[0] && D.topics[0].id;
    if (!id) return;
    renderDetail(id);
    document.querySelectorAll('.topic-list li').forEach(function (li) { li.classList.toggle('on', li.dataset.id === id); });
  }

  function renderList() {
    const q = document.getElementById('q').value.trim().toLowerCase();
    const band = document.getElementById('band').value;
    const box = document.getElementById('list');
    box.textContent = '';
    const groups = [];
    const gmap = {};
    D.topics.forEach(function (t) {
      if (band && t.band !== band) return;
      if (q) {
        const hay = (t.name + ' ' + t.id + ' ' + t.chapter + ' ' + t.standards.map(function (s) { return s.id; }).join(' ')).toLowerCase();
        if (hay.indexOf(q) < 0) return;
      }
      const key = t.chapter;
      if (!gmap[key]) { gmap[key] = { key: key, items: [] }; groups.push(gmap[key]); }
      gmap[key].items.push(t);
    });
    if (!groups.length) { box.append(h('p', { class: 'muted', text: 'No topics match.' })); return; }
    const cur = current();
    groups.forEach(function (g) {
      const det = h('details', { class: 'group', open: true },
        h('summary', null, QM.chapterLabel(g.key), ' ', h('span', { class: 'muted small', text: '(' + g.items.length + ')' })),
        h('ul', { class: 'topic-list' }, g.items.map(function (t) {
          return h('li', { 'data-id': t.id, class: t.id === cur ? 'on' : null, onclick: function () { location.hash = t.id; } },
            h('span', { text: t.name }), h('span', { class: 'tid', text: t.id }));
        })));
      box.append(det);
    });
  }

  function topicLink(id) {
    const t = byId[id];
    return h('a', { href: '#' + id, text: t ? t.name : id });
  }

  function edgeItem(d, otherId) {
    return h('li', null, h('span', { class: 'tag ' + d.strength, text: d.strength }), ' ', topicLink(otherId), ' ',
      QM.bandTag(byId[otherId]), h('div', { class: 'muted small', text: d.reason }));
  }

  function renderDetail(id) {
    const t = byId[id];
    const box = document.getElementById('detail');
    box.textContent = '';
    document.title = t.name + ' · Explore · QLD Maths Taxonomy';
    const head = h('div', { class: 'card' },
      h('div', { class: 'row' }, QM.bandTag(t), h('span', { class: 'tag', text: TYPE_LABEL[t.type] || t.type }),
        h('span', { class: 'tag', text: TECH_LABEL[t.tech] || t.tech }),
        h('span', { class: 'tag ' + (t.status === 'reviewed' ? 'mastered' : 'shaky'), text: t.status === 'reviewed' ? 'Teacher-reviewed' : 'Draft' }),
        h('span', { class: 'spacer' }), h('code', { text: t.id })),
      h('h1', { text: t.name, style: 'margin-top:10px' }),
      h('p', { class: 'muted', text: QM.chapterLabel(t.chapter) }),
      h('p', { text: t.description }),
      h('h3', { text: 'A student who has mastered this can:' }),
      h('ul', null, t.mastery_criteria.map(function (m) { return h('li', { text: m }); })),
      t.root_reason ? h('p', { class: 'small muted', text: 'Starting point: ' + t.root_reason }) : null,
      h('div', { class: 'row' },
        h('a', { class: 'btn primary', href: '../diagnose/?target=' + id, text: 'Diagnose this topic' }),
        h('a', { class: 'btn', href: '../diagnose/?target=' + id + '&demo=1', text: 'Demo' })));
    box.append(head);

    // graph
    const depthSel = h('select', { 'aria-label': 'Levels of prerequisites', style: 'width:auto', onchange: function (e) { depthUp = +e.target.value; drawGraph(id); } },
      [['1', '1 level up'], ['2', '2 levels up'], ['99', 'All prerequisites']].map(function (o) {
        return h('option', { value: o[0], text: o[1], selected: String(depthUp) === o[0] });
      }));
    box.append(h('div', { class: 'card' },
      h('div', { class: 'row' }, h('h2', { text: 'Prerequisite map', style: 'margin:0' }), h('span', { class: 'spacer' }), depthSel),
      h('p', { class: 'muted small', text: 'Prerequisites above, topics that build on this one below. Click a box to open it.' }),
      h('div', { class: 'graph-box' }, h('div', { class: 'cy', id: 'cy' })),
      h('div', { class: 'legend' }, h('span', null, h('i'), 'hard prerequisite'), h('span', null, h('i', { class: 'soft' }), 'soft prerequisite'),
        QM.BANDS.map(function (b) { return h('span', { class: 'tag ' + b.id, text: b.label }); }))));

    // edges
    box.append(h('div', { class: 'card' },
      h('h2', { text: 'Needs (' + prereqs[id].length + ')' }),
      prereqs[id].length ? h('ul', { class: 'edge-list' }, prereqs[id].map(function (d) { return edgeItem(d, d.prerequisiteId); }))
        : h('p', { class: 'muted', text: 'No prerequisites in this map.' }),
      h('h2', { text: 'Leads to (' + dependents[id].length + ')', style: 'margin-top:14px' }),
      dependents[id].length ? h('ul', { class: 'edge-list' }, dependents[id].map(function (d) { return edgeItem(d, d.topicId); }))
        : h('p', { class: 'muted', text: 'Nothing builds on this topic yet.' })));

    // standards
    box.append(h('div', { class: 'card' }, h('h2', { text: 'Curriculum' }),
      h('ul', { class: 'edge-list' }, t.standards.map(function (s) {
        const it = D.stdById[s.id] || {};
        return h('li', null, h('code', { text: s.id }), ' ', h('span', { class: 'tag', text: s.confidence }), ' ',
          h('span', { text: it.text || '' }),
          h('div', { class: 'muted small', text: (it.source || '') + (it.verbatim === false ? ' · paraphrase, not official wording' : '') +
            (it.title_status === 'unverified' || it.status === 'inferred' ? ' · to verify' : '') }));
      }))));

    // sample questions
    const qs = qByTopic[id];
    if (qs.length) {
      box.append(h('div', { class: 'card' }, h('h2', { text: 'Questions (' + qs.length + ')' }),
        qs.map(function (q) {
          const ans = q.type === 'choice' ? q.answer + '. ' + (q.choices.find(function (c) { return c.key === q.answer; }) || {}).text : q.answer;
          return h('details', { class: 'group' },
            h('summary', null, h('span', { class: 'tag', text: q.difficulty }), ' ', q.prompt),
            q.choices ? h('ol', { type: 'A' }, q.choices.map(function (c) { return h('li', { text: c.text }); })) : null,
            h('p', null, h('b', { text: 'Answer: ' }), ans),
            h('p', { class: 'muted small', text: q.explanation }),
            h('p', { class: 'small muted' }, h('code', { text: q.id })));
        })));
    }
    drawGraph(id);
  }

  function collect(id) {
    const nodes = new Set([id]);
    let frontier = [id];
    for (let d = 0; d < depthUp && frontier.length; d++) {
      const next = [];
      frontier.forEach(function (n) { prereqs[n].forEach(function (e) { if (!nodes.has(e.prerequisiteId)) { nodes.add(e.prerequisiteId); next.push(e.prerequisiteId); } }); });
      frontier = next;
    }
    dependents[id].forEach(function (e) { nodes.add(e.topicId); });
    const edges = D.deps.filter(function (e) { return nodes.has(e.topicId) && nodes.has(e.prerequisiteId); });
    return { nodes: Array.from(nodes), edges: edges };
  }

  function drawGraph(id) {
    if (cy) { cy.destroy(); cy = null; }
    const el = document.getElementById('cy');
    if (!el || !window.cytoscape) return;
    if (window.cytoscapeDagre && !drawGraph.reg) { window.cytoscape.use(window.cytoscapeDagre); drawGraph.reg = true; }
    const g = collect(id);
    const elements = g.nodes.map(function (n) {
      const t = byId[n];
      const c = QM.bandColors(t.band);
      return { data: { id: n, label: QM.clip(t.name, 34), fg: c.fg, bg: c.bg, cur: n === id ? 1 : 0 } };
    }).concat(g.edges.map(function (e) {
      return { data: { id: e.prerequisiteId + '>' + e.topicId, source: e.prerequisiteId, target: e.topicId, strength: e.strength } };
    }));
    const text = QM.cssVar('--text');
    cy = window.cytoscape({
      container: el, elements: elements, wheelSensitivity: 0.3, minZoom: 0.3, maxZoom: 2,
      style: [
        { selector: 'node', style: { shape: 'round-rectangle', 'background-color': 'data(bg)', 'border-color': 'data(fg)', 'border-width': 1.5,
          label: 'data(label)', color: text, 'font-size': 11, 'text-wrap': 'wrap', 'text-max-width': 130, 'text-valign': 'center',
          width: 150, height: 44, padding: 4 } },
        { selector: 'node[cur = 1]', style: { 'border-width': 4, 'font-weight': 700 } },
        { selector: 'edge', style: { width: 1.6, 'line-color': QM.cssVar('--edge'), 'target-arrow-color': QM.cssVar('--edge'),
          'target-arrow-shape': 'triangle', 'curve-style': 'bezier' } },
        { selector: 'edge[strength = "soft"]', style: { 'line-style': 'dashed', 'line-color': QM.cssVar('--edge-soft'), 'target-arrow-color': QM.cssVar('--edge-soft') } }
      ],
      layout: window.cytoscapeDagre ? { name: 'dagre', rankDir: 'TB', nodeSep: 18, rankSep: 46 } : { name: 'breadthfirst', directed: true }
    });
    cy.on('tap', 'node', function (e) { location.hash = e.target.id(); });
    cy.fit(undefined, 20);
  }
})();
