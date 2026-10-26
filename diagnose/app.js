/* Diagnose UI: start page, question page, results. The algorithm lives in engine.js. */
(function () {
  'use strict';
  const E = window.DiagEngine;
  const h = QM.h;
  const LS_SESSION = 'qmDiagnose.session.v1';
  const LS_SEEN = 'qmDiagnose.seen.v1';
  const LS_SETTINGS = 'qmDiagnose.settings.v1';
  const STATUS_LABEL = { mastered: 'Mastered', shaky: 'Shaky', weak: 'Weak', unknown: 'Not tested' };
  const DIFF_LABEL = { basic: 'Basic', standard: 'Standard', advanced: 'Advanced' };
  const root = document.getElementById('root');
  const params = new URLSearchParams(location.search);
  const demo = params.get('demo') === '1';
  const seedParam = params.get('seed');

  let D, G;            // data, engine graph
  let S = null;        // current session meta {targets, mode, label, limit, seed}
  let session = null;  // engine session
  let ui = {};         // per-question UI state
  let cy = null;

  QM.loadData('../').then(function (data) {
    D = data;
    G = E.buildGraph(D.topics, D.deps, D.questions);
    boot();
  }).catch(function (e) { root.textContent = 'Could not load data: ' + e.message; });

  function nameOf(id) { const t = G.byId[id]; return t ? t.name : id; }
  function settings() { return QM.lsGet(LS_SETTINGS) || {}; }
  function seenList() { const v = QM.lsGet(LS_SEEN); return Array.isArray(v) ? v : []; }
  function markSeen(qid) {
    if (demo || !qid) return;
    const s = seenList();
    if (s.indexOf(qid) < 0) { s.push(qid); QM.lsSet(LS_SEEN, s.slice(-2000)); }
  }
  function show(node) { if (cy) { cy.destroy(); cy = null; } root.textContent = ''; root.append(node); window.scrollTo(0, 0); }

  /* ------------------------------------------------------------ session handling */

  function boot() {
    const rawTargets = (params.get('target') || '').split(',').map(function (s) { return s.trim(); }).filter(Boolean);
    const scope = params.get('scope');
    const limit = params.get('limit') ? Math.max(4, Math.min(80, +params.get('limit'))) : null;
    if (rawTargets.length) {
      const ids = E.resolveTargets(rawTargets, D.aliases);
      const bad = ids.filter(function (id) { return !G.byId[id]; });
      if (bad.length) return renderStart('Unknown topic id: ' + bad.join(', '));
      return startOrResume({ targets: ids, mode: 'target', label: ids.map(nameOf).join(', '), limit: limit });
    }
    if (scope) {
      const g = E.gradeTargets(G, scope);
      if (!g) return renderStart('No topics found for “' + scope + '”.');
      return startOrResume({ targets: g.ids, mode: 'screen', label: g.label, limit: limit });
    }
    renderStart();
  }

  function sameTargets(a, b) { return a && b && a.mode === b.mode && a.targets.join(',') === b.targets.join(','); }

  function startOrResume(spec) {
    const saved = QM.lsGet(LS_SESSION);
    if (!demo && saved && sameTargets(saved, spec) && saved.answers && saved.answers.length) return restore(saved);
    start(spec);
  }

  function start(spec) {
    const st = settings();
    const screen = spec.mode === 'screen';
    S = {
      targets: spec.targets, mode: spec.mode, label: spec.label,
      limit: spec.limit || (screen ? (st.screenLimit || E.SCREEN_LIMIT) : (st.limit || E.DEFAULT_LIMIT)),
      seed: seedParam != null ? seedParam : (demo ? 'demo' : Math.random().toString(36).slice(2, 10))
    };
    session = E.createSession(G, S.targets, { limit: S.limit, seed: S.seed, avoid: demo ? [] : seenList(), mode: screen ? 'screen' : undefined });
    if (demo) return runDemo();
    save();
    renderNext();
  }

  function restore(saved) {
    S = { targets: saved.targets, mode: saved.mode, label: saved.label, limit: saved.limit, seed: saved.seed };
    session = E.replay(G, S.targets, saved.answers, { limit: S.limit, seed: S.seed, avoid: saved.avoid || [], mode: S.mode === 'screen' ? 'screen' : undefined });
    renderNext();
  }

  function save() {
    if (demo) return;
    QM.lsSet(LS_SESSION, Object.assign({}, S, { answers: session.answers, avoid: session.avoid }));
  }

  function rebuild(answers, limit) {
    if (limit) S.limit = limit;
    session = E.replay(G, S.targets, answers, { limit: S.limit, seed: S.seed, avoid: session.avoid, mode: S.mode === 'screen' ? 'screen' : undefined });
    save();
    renderNext();
  }

  function commit(result, text) {
    const item = E.nextItem(G, session);
    if (!item) return;
    markSeen(item.question.id);
    session = E.applyAnswer(G, session, item.topicId, result, { text: text });
    save();
    ui = {};
    renderNext();
  }

  function renderNext() {
    const item = E.nextItem(G, session);
    if (item) renderQuestion(item); else renderResult();
  }

  /* ------------------------------------------------------------ demo: a simulated student */

  function runDemo() {
    // Target missed twice; its first testable prerequisite missed twice (root cause);
    // the next prerequisite wrong then right (shaky); everything else right. Screening: by position.
    const plan = {};
    if (S.mode === 'screen') {
      S.targets.forEach(function (id, i) { plan[id] = i % 6 === 2 ? ['wrong', 'wrong'] : i % 6 === 4 ? ['wrong', 'correct'] : ['correct']; });
    } else {
      const t = S.targets[0];
      plan[t] = ['wrong', 'wrong'];
      const p = G.prereqs[t].map(function (e) { return e.id; }).filter(function (id) { return E.isTestable(G, id); });
      if (p[0]) {
        plan[p[0]] = ['wrong', 'wrong'];
        const pp = G.prereqs[p[0]].map(function (e) { return e.id; }).filter(function (id) { return E.isTestable(G, id); });
        const shaky = pp[0] || p[1];
        if (shaky) plan[shaky] = ['wrong', 'correct'];
      }
    }
    const steps = params.get('step') ? +params.get('step') : Infinity;
    let n = 0;
    for (let item = E.nextItem(G, session); item && n < steps; item = E.nextItem(G, session), n++) {
      const seq = plan[item.topicId] || ['correct'];
      const r = seq[Math.min(item.attempt - 1, seq.length - 1)];
      session = E.applyAnswer(G, session, item.topicId, r, { text: r === 'correct' ? item.question.answer : '' });
    }
    renderNext();
  }

  /* ------------------------------------------------------------ start page */

  function renderStart(errMsg) {
    const saved = QM.lsGet(LS_SESSION);
    const page = h('div');
    if (errMsg) page.append(h('div', { class: 'card error', text: errMsg }));
    if (saved && saved.answers && saved.answers.length) {
      page.append(h('div', { class: 'card' }, h('h2', { text: 'Unfinished diagnosis' }),
        h('p', null, saved.label + ' · ' + saved.answers.length + ' questions answered'),
        h('div', { class: 'row' },
          h('button', { class: 'btn primary', text: 'Continue', onclick: function () { restore(saved); } }),
          h('button', { class: 'btn', text: 'Discard', onclick: function () { QM.lsDel(LS_SESSION); renderStart(); } }))));
    }

    // whole level / unit
    const vols = [];
    D.topics.forEach(function (t) { const v = QM.volumeOf(t); if (vols.indexOf(v) < 0) vols.push(v); });
    page.append(h('div', { class: 'card' },
      h('h2', { text: 'Check a whole level or unit' }),
      h('p', { class: 'muted small', text: 'Screening mode: questions stay inside the chosen level. A correct answer also clears the earlier topics it depends on.' }),
      h('div', { class: 'row' }, vols.map(function (v) {
        const g = E.gradeTargets(G, v);
        return h('button', { class: 'btn', onclick: function () { go({ scope: v }); } }, v, ' ', h('span', { class: 'muted small', text: '(' + g.ids.length + ')' }));
      }))));

    // single topic
    const search = h('input', { type: 'search', placeholder: 'Search for a topic, e.g. quadratic formula', 'aria-label': 'Search topics' });
    const list = h('div');
    const fill = function () {
      const q = search.value.trim().toLowerCase();
      list.textContent = '';
      const groups = {};
      const order = [];
      D.topics.forEach(function (t) {
        if (q && (t.name + ' ' + t.id + ' ' + t.chapter).toLowerCase().indexOf(q) < 0) return;
        if (!groups[t.chapter]) { groups[t.chapter] = []; order.push(t.chapter); }
        groups[t.chapter].push(t);
      });
      order.forEach(function (c) {
        list.append(h('details', { class: 'group', open: !!q || order.length <= 3 }, h('summary', { text: c + ' (' + groups[c].length + ')' }),
          h('ul', { class: 'topic-list' }, groups[c].map(function (t) {
            return h('li', { onclick: function () { go({ target: t.id }); } }, h('span', { text: t.name }), h('span', { class: 'tid', text: 'Start →' }));
          }))));
      });
      if (!order.length) list.append(h('p', { class: 'muted', text: 'No topics match.' }));
    };
    search.addEventListener('input', fill);
    fill();
    const st = settings();
    const lim = h('input', { type: 'number', min: 8, max: 40, value: st.limit || E.DEFAULT_LIMIT, style: 'width:90px',
      onchange: function (e) { const o = settings(); o.limit = Math.max(8, Math.min(40, +e.target.value || E.DEFAULT_LIMIT)); QM.lsSet(LS_SETTINGS, o); } });
    page.append(h('div', { class: 'card' },
      h('h2', { text: 'Diagnose one topic' }),
      h('p', { class: 'muted small', text: 'Choose the topic the student is struggling with. The tool starts there and works back through its prerequisites.' }),
      h('div', { class: 'row', style: 'margin-bottom:8px' }, h('label', { class: 'small muted', text: 'Question limit' }), lim),
      search, list));
    show(page);
  }

  function go(q) {
    const u = new URL(location.href);
    u.search = '';
    Object.keys(q).forEach(function (k) { u.searchParams.set(k, q[k]); });
    location.href = u.toString();
  }

  /* ------------------------------------------------------------ question page */

  function reasonFor(item) {
    if (item.attempt === 2) return 'Second try: the first question on this topic was missed.';
    if (S.mode !== 'screen' && S.targets.indexOf(item.topicId) >= 0) return 'This is the target topic.';
    const parent = G.dependents[item.topicId].map(function (d) { return d.id; })
      .find(function (id) { return session.status[id] && session.status[id].s === 'weak'; });
    if (parent) return 'Checking a prerequisite of “' + nameOf(parent) + '”, which was missed twice.';
    return S.mode === 'screen' ? 'Next topic in ' + S.label + '.' : 'Checking an earlier topic.';
  }

  function answerText(q) {
    if (q.type !== 'choice') return q.answer;
    const c = (q.choices || []).find(function (x) { return x.key === q.answer; });
    return q.answer + '. ' + (c ? c.text : '');
  }

  function renderQuestion(item) {
    const q = item.question;
    const t = G.byId[item.topicId];
    const asked = session.answers.length;
    const card = h('div', { class: 'card' });
    card.append(h('div', { class: 'row' },
      h('span', { class: 'muted small', text: 'Question ' + (asked + 1) + ' of at most ' + S.limit }),
      h('span', { class: 'spacer' }),
      h('button', { class: 'btn small', text: 'Undo', disabled: !asked || null, onclick: function () { rebuild(session.answers.slice(0, -1)); } }),
      h('button', { class: 'btn small', text: 'See results now', onclick: function () { renderResult(true); } })));
    card.append(h('div', { class: 'progress' }, h('span', { style: 'width:' + Math.round(100 * asked / S.limit) + '%' })));
    card.append(h('div', { class: 'row' }, QM.bandTag(t), h('b', { text: t.name }),
      h('span', { class: 'tag', text: DIFF_LABEL[q.difficulty] || q.difficulty }),
      q.tech === 'active' ? h('span', { class: 'tag', text: 'Calculator allowed' }) : null));
    card.append(h('p', { class: 'why', text: reasonFor(item) }));
    card.append(h('div', { class: 'question', text: q.prompt }));

    const fb = h('div');
    const done = function (verdict) {
      ui.verdict = verdict;
      renderFeedback(fb, item, verdict);
    };

    if (q.type === 'choice') {
      const btns = q.choices.map(function (c) {
        return h('button', { class: 'btn choice', 'data-key': c.key, onclick: function () {
          if (ui.verdict) return;
          ui.text = c.key;
          btns.forEach(function (b) { b.classList.toggle('picked', b.dataset.key === c.key); });
          const v = E.judgeQuestion(q, c.key).verdict;
          btns.forEach(function (b) {
            if (b.dataset.key === q.answer) b.classList.add('correct');
            else if (b.dataset.key === c.key) b.classList.add('wrong');
          });
          done(v);
        } }, h('b', { text: c.key + '.' }), ' ', c.text);
      });
      card.append(h('div', { class: 'choices' }, btns));
    } else {
      const input = h('input', { type: 'text', autocomplete: 'off', placeholder: q.answer.indexOf('(') === 0 ? 'e.g. (2, -1)' : 'Your answer', 'aria-label': 'Your answer' });
      const submit = function () {
        if (ui.verdict) return;
        ui.text = input.value;
        done(E.judgeQuestion(q, input.value).verdict);
      };
      input.addEventListener('keydown', function (e) { if (e.key === 'Enter') submit(); });
      card.append(h('div', { class: 'row' }, h('div', { style: 'flex:1;min-width:180px' }, input),
        h('button', { class: 'btn primary', text: 'Check', onclick: submit })));
      if (q.unordered) card.append(h('p', { class: 'muted small', text: 'Several answers: separate them with commas, in any order.' }));
      setTimeout(function () { input.focus(); }, 0);
    }
    card.append(h('div', { class: 'row', style: 'margin-top:10px' },
      h('button', { class: 'btn small', text: "I don't know", onclick: function () { if (!ui.verdict) { ui.text = ''; done('skip'); } } })));
    card.append(fb);
    card.append(h('p', { class: 'muted small', style: 'margin-top:12px' }, 'Question id ', h('code', { text: q.id })));
    show(card);
  }

  function renderFeedback(box, item, verdict) {
    const q = item.question;
    box.textContent = '';
    const cls = verdict === 'correct' ? 'correct' : verdict === 'manual' ? 'manual' : 'wrong';
    const title = verdict === 'correct' ? 'Correct' : verdict === 'wrong' ? 'Not quite' : verdict === 'skip' ? 'Here is the worked answer' : 'Compare with the worked answer';
    const fb = h('div', { class: 'feedback ' + cls }, h('b', { text: title }),
      h('p', { style: 'margin:6px 0 4px' }, 'Answer: ', h('b', { text: answerText(q) })),
      q.explanation ? h('p', { class: 'small', text: q.explanation }) : null);
    const next = function (r) { commit(r, ui.text); };
    if (verdict === 'manual') {
      fb.append(h('div', { class: 'row' },
        h('button', { class: 'btn primary', text: 'I was right', onclick: function () { next('correct'); } }),
        h('button', { class: 'btn', text: 'I was wrong', onclick: function () { next('wrong'); } })));
    } else {
      const res = verdict === 'skip' ? 'skip' : verdict;
      fb.append(h('div', { class: 'row' },
        h('button', { class: 'btn primary', text: 'Next', onclick: function () { next(res); } }),
        verdict !== 'skip' ? h('button', { class: 'btn small', text: verdict === 'correct' ? 'Actually I was wrong' : 'Actually I was right',
          onclick: function () { next(verdict === 'correct' ? 'wrong' : 'correct'); } }) : null));
    }
    box.append(fb);
    const btn = fb.querySelector('.btn.primary');
    if (btn) btn.focus();
  }

  /* ------------------------------------------------------------ results */

  function tag(cls, text) { return h('span', { class: 'tag ' + cls, text: text }); }

  function topicLine(id, extra) {
    const t = G.byId[id];
    return h('span', null, h('a', { href: '../explore/#' + id, text: t.name }), ' ', QM.bandTag(t), extra || null);
  }

  function renderResult(early) {
    const sum = E.summarize(G, session);
    const page = h('div');
    const screen = S.mode === 'screen';
    page.append(h('div', { class: 'card' },
      h('div', { class: 'row' }, h('h1', { text: 'Results', style: 'margin:0' }), h('span', { class: 'spacer' }),
        demo ? tag('shaky', 'Demo: simulated student') : null),
      h('p', { class: 'muted', text: (screen ? 'Checked: ' : 'Target: ') + S.label + ' · ' + sum.asked + ' questions' + (early && !sum.finished ? ' · stopped early' : '') }),
      h('div', { class: 'result-stats' },
        h('div', { class: 'stat ok' }, h('b', { text: String(sum.mastered.length) }), 'mastered'),
        h('div', { class: 'stat shaky' }, h('b', { text: String(sum.shaky.length) }), 'shaky'),
        h('div', { class: 'stat bad' }, h('b', { text: String(sum.weak.length) }), 'weak'),
        h('div', { class: 'stat' }, h('b', { text: String(sum.untested.length) }), 'not tested')),
      sum.limitReached ? h('div', { class: 'row', style: 'margin-top:10px' },
        h('span', { class: 'muted small', text: 'The question limit was reached before everything was checked.' }),
        h('button', { class: 'btn small', text: 'Answer 4 more', onclick: function () { rebuild(session.answers, S.limit + 4); } })) : null,
      !sum.finished && !sum.limitReached ? h('button', { class: 'btn small', text: 'Back to the questions', onclick: renderNext }) : null));

    // root causes
    const rootsCard = h('div', { class: 'card' }, h('h2', { text: 'Where the gap starts' }));
    if (!sum.roots.length) {
      rootsCard.append(h('p', { text: sum.weak.length ? 'No single starting point was found.' : 'No weak topics found. ' + (sum.shaky.length ? 'Some topics are shaky; see the learning path.' : 'Nice work.') }));
    } else {
      rootsCard.append(h('ul', { class: 'edge-list' }, sum.roots.map(function (r) {
        const notes = [];
        if (r.pendingPrereqs.length) notes.push('Not all of its prerequisites were tested, so the gap may start earlier: ' + r.pendingPrereqs.map(nameOf).join(', ') + '.');
        if (r.outOfScopePrereqs.length) notes.push('Prerequisites outside this check: ' + r.outOfScopePrereqs.map(nameOf).join(', ') + '. Diagnose this topic on its own to look further back.');
        if (E.isUnconfirmed(session, r.id)) notes.push('Only one question was asked before the limit.');
        return h('li', null, tag('root', 'Root cause'), ' ', topicLine(r.id),
          h('div', { class: 'muted small', text: G.byId[r.id].description }),
          notes.map(function (n) { return h('div', { class: 'small', text: n }); }));
      })));
    }
    page.append(rootsCard);

    // learning path
    if (sum.path.length) {
      page.append(h('div', { class: 'card' }, h('h2', { text: 'Learning path' }),
        h('p', { class: 'muted small', text: 'Work through these in order. Topics marked “not tested” are worth a quick self-check first.' }),
        h('ol', { class: 'path-list' }, sum.path.map(function (p) {
          return h('li', null, topicLine(p.id), ' ', tag(p.status, STATUS_LABEL[p.status]),
            p.isRoot ? [' ', tag('root', 'root cause')] : null, p.isTarget ? [' ', tag('target', 'target')] : null);
        }))));
    }

    // chapter summary for screening
    if (screen) {
      const chs = E.chapterSummary(G, session);
      page.append(h('div', { class: 'card' }, h('h2', { text: 'By topic group' }),
        chs.map(function (c) {
          const w = function (n) { return (100 * n / c.total) + '%'; };
          return h('div', { style: 'margin:10px 0' },
            h('div', { class: 'row' }, h('b', { text: c.label }), h('span', { class: 'spacer' }),
              h('span', { class: 'small muted', text: c.mastered + ' mastered · ' + c.shaky + ' shaky · ' + c.weak + ' weak · ' + c.untested + ' not tested' })),
            h('div', { class: 'bar' }, h('span', { class: 'm', style: 'width:' + w(c.mastered) }), h('span', { class: 's', style: 'width:' + w(c.shaky) }),
              h('span', { class: 'w', style: 'width:' + w(c.weak) })),
            c.weakIds.length ? h('div', { class: 'small', text: 'Weak: ' + c.weakIds.map(nameOf).join(', ') }) : null);
        })));
    }

    // path graph
    const graphCard = h('div', { class: 'card' }, h('h2', { text: 'Map of this diagnosis' }),
      h('div', { class: 'graph-box' }, h('div', { class: 'cy', id: 'cy' })),
      h('div', { class: 'legend' }, tag('mastered', 'mastered'), tag('shaky', 'shaky'), tag('weak', 'weak'), tag('unknown', 'not tested'),
        h('span', null, h('i'), 'hard'), h('span', null, h('i', { class: 'soft' }), 'soft'), h('span', null, h('i', { class: 'indirect' }), 'via other topics')));
    page.append(graphCard);

    // answer log
    page.append(h('div', { class: 'card' }, h('h2', { text: 'Answers' }),
      h('table', { class: 'log' }, h('tr', null, h('th', { text: '#' }), h('th', { text: 'Topic' }), h('th', { text: 'Question' }), h('th', { text: 'Result' }), h('th')),
        session.answers.map(function (a, i) {
          const q = E.questionById(G, a.qid);
          return h('tr', null, h('td', { text: String(i + 1) }), h('td', { text: nameOf(a.id) }),
            h('td', null, q ? q.prompt : a.qid, a.text ? h('div', { class: 'muted small', text: 'Answered: ' + a.text }) : null,
              q ? h('div', { class: 'muted small', text: 'Answer: ' + answerText(q) }) : null),
            h('td', null, tag(a.result === 'correct' ? 'mastered' : 'weak', a.result === 'skip' ? "didn't know" : a.result)),
            h('td', null, demo ? null : h('button', { class: 'btn small', text: 'Flip', title: 'Correct a mis-marked answer', onclick: function () {
              const answers = session.answers.map(function (x, j) { return j === i ? Object.assign({}, x, { result: x.result === 'correct' ? 'wrong' : 'correct' }) : x; });
              rebuild(answers.map(function (x) { return { id: x.id, result: x.result, text: x.text }; }));
            } })));
        }))));

    page.append(h('div', { class: 'row no-print' },
      h('button', { class: 'btn', text: 'Print / save as PDF', onclick: function () { window.print(); } }),
      h('button', { class: 'btn', text: 'Export JSON', onclick: exportJson }),
      h('button', { class: 'btn', text: 'New diagnosis', onclick: function () { if (!demo) QM.lsDel(LS_SESSION); go({}); } })));
    show(page);
    drawPath(sum);
  }

  function drawPath(sum) {
    const el = document.getElementById('cy');
    if (!el || !window.cytoscape) return;
    if (window.cytoscapeDagre && !drawPath.reg) { window.cytoscape.use(window.cytoscapeDagre); drawPath.reg = true; }
    const lay = E.layout(G, session, sum);
    const col = { mastered: ['--ok', '--ok-bg'], shaky: ['--warn', '--warn-bg'], weak: ['--bad', '--bad-bg'], unknown: ['--unk', '--unk-bg'] };
    const els = lay.nodes.map(function (n) {
      const c = col[n.status] || col.unknown;
      return { data: { id: n.id, label: QM.clip(nameOf(n.id), 34) + (n.isRoot ? '\n(root cause)' : n.isTarget ? '\n(target)' : ''),
        fg: QM.cssVar(c[0]), bg: QM.cssVar(c[1]), bw: n.isRoot || n.isTarget ? 4 : 1.5 } };
    }).concat(lay.edges.map(function (e) {
      return { data: { id: e.from + '>' + e.to, source: e.from, target: e.to, kind: e.direct ? e.strength : 'indirect' } };
    }));
    cy = window.cytoscape({
      container: el, elements: els, minZoom: 0.3, maxZoom: 2, wheelSensitivity: 0.3,
      style: [
        { selector: 'node', style: { shape: 'round-rectangle', 'background-color': 'data(bg)', 'border-color': 'data(fg)', 'border-width': 'data(bw)',
          label: 'data(label)', color: QM.cssVar('--text'), 'font-size': 11, 'text-wrap': 'wrap', 'text-max-width': 130, 'text-valign': 'center',
          width: 150, height: 48 } },
        { selector: 'edge', style: { width: 1.6, 'line-color': QM.cssVar('--edge'), 'target-arrow-color': QM.cssVar('--edge'), 'target-arrow-shape': 'triangle', 'curve-style': 'bezier' } },
        { selector: 'edge[kind = "soft"]', style: { 'line-style': 'dashed', 'line-color': QM.cssVar('--edge-soft'), 'target-arrow-color': QM.cssVar('--edge-soft') } },
        { selector: 'edge[kind = "indirect"]', style: { 'line-style': 'dotted', 'line-color': QM.cssVar('--edge-soft'), 'target-arrow-color': QM.cssVar('--edge-soft') } }
      ],
      layout: window.cytoscapeDagre ? { name: 'dagre', rankDir: 'TB', nodeSep: 18, rankSep: 46 } : { name: 'breadthfirst', directed: true }
    });
    cy.on('tap', 'node', function (e) { window.open('../explore/#' + e.target.id(), '_blank'); });
    cy.fit(undefined, 20);
  }

  function exportJson() {
    const sum = E.summarize(G, session);
    const out = {
      exported: new Date().toISOString(), scope: S.label, mode: S.mode, targets: S.targets, seed: S.seed,
      roots: sum.roots.map(function (r) { return { id: r.id, name: nameOf(r.id) }; }),
      path: sum.path.map(function (p) { return { id: p.id, name: nameOf(p.id), status: p.status }; }),
      answers: session.answers.map(function (a) {
        const q = E.questionById(G, a.qid);
        return { topic: a.id, question: a.qid, result: a.result, answered: a.text || '', answer: q ? answerText(q) : '' };
      })
    };
    const blob = new Blob([JSON.stringify(out, null, 2)], { type: 'application/json' });
    const a = h('a', { href: URL.createObjectURL(blob), download: 'diagnosis-' + new Date().toISOString().slice(0, 10) + '.json' });
    document.body.append(a); a.click(); a.remove();
  }
})();
