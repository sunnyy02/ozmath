/* Diagnosis engine: pure functions, no DOM, no dependencies. window.DiagEngine in the browser, require() in Node.
 * Forked from cn-math-taxonomy (CC BY-NC 4.0, https://github.com/xiaoyang111222/cn-math-taxonomy);
 * the adaptive algorithm is unchanged, labels, chapter parsing, ranking and answer judging are adapted for QLD.
 *
 * Data flow: buildGraph(topics, deps, questions?) -> graph
 *            createSession(graph, targets, {limit, seed, avoid, mode}) -> session (plain JSON)
 *            nextItem(graph, session) -> {topicId, question, attempt} | null
 *            applyAnswer(graph, session, id, 'correct'|'wrong'|'skip', {text}) -> new session
 *            summarize(graph, session) -> root causes, learning path, mastered / shaky / weak / untested
 *            gradeTargets(graph, 'Year 10' | 'Methods U1' | 'Methods') -> {ids, volumes, label} | null
 *            chapterSummary, layout, judgeQuestion, judgeAnswer
 *
 * At most 2 questions per topic. 1st correct -> mastered (ancestors inferred mastered). 1st wrong -> a 2nd, easier
 * question: correct -> shaky (no backtracking); wrong -> weak, and its prerequisites (hard before soft) are tested next.
 */
(function (root, factory) {
  if (typeof module !== 'undefined' && module.exports) module.exports = factory();
  else root.DiagEngine = factory();
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  /* ------------------------------------------------------------------ graph */

  const DIFF_RANK = { basic: 0, standard: 1, advanced: 2 };

  function qNum(q) { const m = /_q(\d+)$/.exec(q.id); return m ? parseInt(m[1], 10) : 0; }

  function buildGraph(topics, deps, questions) {
    const byId = Object.create(null);
    const index = Object.create(null);
    topics.forEach(function (t, i) { byId[t.id] = t; index[t.id] = i; });
    const prereqs = Object.create(null);
    const dependents = Object.create(null);
    topics.forEach(function (t) { prereqs[t.id] = []; dependents[t.id] = []; });
    const seen = Object.create(null);
    deps.forEach(function (d) {
      if (!byId[d.topicId] || !byId[d.prerequisiteId]) return;
      const k = d.topicId + '<' + d.prerequisiteId;
      if (seen[k]) return;
      seen[k] = true;
      const strength = d.strength === 'soft' ? 'soft' : 'hard';
      prereqs[d.topicId].push({ id: d.prerequisiteId, strength: strength, reason: d.reason });
      dependents[d.prerequisiteId].push({ id: d.topicId, strength: strength });
    });
    // prerequisites: hard before soft, then topics-file order, so question order is deterministic
    const rank = function (e) { return (e.strength === 'hard' ? 0 : 1) * 1e6 + index[e.id]; };
    Object.keys(prereqs).forEach(function (id) {
      prereqs[id].sort(function (a, b) { return rank(a) - rank(b); });
      dependents[id].sort(function (a, b) { return index[a.id] - index[b.id]; });
    });
    // question bank per topic, sorted by question number; falls back to diagnostic_question
    const bank = Object.create(null);
    topics.forEach(function (t) { bank[t.id] = []; });
    let fromFile = 0;
    (Array.isArray(questions) ? questions : []).forEach(function (q) {
      if (q && bank[q.topicId] && !byId[q.topicId].external) { bank[q.topicId].push(q); fromFile++; }
    });
    topics.forEach(function (t) {
      const dq = t.diagnostic_question;
      if (!t.external && !bank[t.id].length && dq && dq.question) {
        bank[t.id].push({ id: t.id + '_q1', topicId: t.id, difficulty: 'standard', type: 'legacy', prompt: dq.question, answer: dq.answer, explanation: '' });
      }
    });
    Object.keys(bank).forEach(function (id) { bank[id].sort(function (a, b) { return qNum(a) - qNum(b); }); });
    return {
      topics: topics, byId: byId, index: index, prereqs: prereqs, dependents: dependents, bank: bank,
      hasBank: fromFile > 0, _anc: Object.create(null)
    };
  }

  /** Strict ancestor set (excluding the topic itself), memoised. */
  function ancestorSet(graph, id) {
    const memo = graph._anc;
    if (memo[id]) return memo[id];
    const visiting = graph._visiting || (graph._visiting = Object.create(null));
    if (visiting[id]) throw new Error('Cycle in prerequisite graph: ' + id);
    visiting[id] = true;
    const out = new Set();
    graph.prereqs[id].forEach(function (p) {
      out.add(p.id);
      ancestorSet(graph, p.id).forEach(function (a) { out.add(a); });
    });
    visiting[id] = false;
    memo[id] = out;
    return out;
  }

  function ancestors(graph, ids) {
    const list = Array.isArray(ids) ? ids : [ids];
    const out = new Set();
    list.forEach(function (id) { ancestorSet(graph, id).forEach(function (a) { out.add(a); }); });
    return out;
  }

  /** Deterministic topological sort of a node subset (prerequisites first). */
  function topoSort(graph, ids) {
    const set = new Set(ids);
    const indeg = Object.create(null);
    set.forEach(function (id) {
      indeg[id] = graph.prereqs[id].filter(function (p) { return set.has(p.id); }).length;
    });
    const ready = [];
    set.forEach(function (id) { if (indeg[id] === 0) ready.push(id); });
    const byIndex = function (a, b) { return graph.index[a] - graph.index[b]; };
    const order = [];
    while (ready.length) {
      ready.sort(byIndex);
      const id = ready.shift();
      order.push(id);
      graph.dependents[id].forEach(function (d) {
        if (!set.has(d.id)) return;
        indeg[d.id] -= 1;
        if (indeg[d.id] === 0) ready.push(d.id);
      });
    }
    if (order.length !== set.size) throw new Error('Topological sort failed: cycle in subgraph');
    return order;
  }

  /** Prerequisite subgraph of the targets: targets + all ancestors, topologically sorted. */
  function subgraph(graph, targets) {
    const set = new Set(targets);
    ancestors(graph, targets).forEach(function (a) { set.add(a); });
    return { nodes: topoSort(graph, set), set: set };
  }

  function isTestable(graph, id) {
    const t = graph.byId[id];
    return !!(t && !t.external && graph.bank[id] && graph.bank[id].length);
  }

  function questionById(graph, qid) {
    const m = /^(.*)_q\d+$/.exec(qid || '');
    const list = m ? graph.bank[m[1]] : null;
    return (list || []).find(function (q) { return q.id === qid; }) || null;
  }

  /* ------------------------------------------------------------------ session */

  const RESULTS = { correct: 1, wrong: 1, skip: 1 };
  const DEFAULT_LIMIT = 16;
  const SCREEN_LIMIT = 40;

  function createSession(graph, targets, opts) {
    opts = opts || {};
    const ts = Array.from(new Set(targets));
    if (!ts.length) throw new Error('At least one target topic is needed');
    ts.forEach(function (id) { if (!graph.byId[id]) throw new Error('Unknown topic: ' + id); });
    const screen = opts.mode === 'screen';
    const limit = Math.max(1, Math.floor(opts.limit == null ? (screen ? SCREEN_LIMIT : DEFAULT_LIMIT) : opts.limit));
    // screening mode: scope is the target set itself; backtracking stays inside it
    const sub = screen ? { nodes: topoSort(graph, ts) } : subgraph(graph, ts);
    const pos = Object.create(null);
    sub.nodes.forEach(function (id, i) { pos[id] = i; });
    // ask the target nearest the end of the topological order first; the rest wait on the stack
    const stack = ts.filter(function (id) { return isTestable(graph, id); })
      .sort(function (a, b) { return pos[b] - pos[a]; });
    return {
      targets: ts, limit: limit, order: sub.nodes, status: {}, stack: stack, answers: [], attempts: {},
      mode: screen ? 'screen' : 'target', scope: screen ? ts.slice() : null,
      seed: opts.seed == null ? 'default' : String(opts.seed),
      avoid: Array.from(new Set(opts.avoid || []))
    };
  }

  function cloneSession(s) {
    const attempts = {};
    Object.keys(s.attempts).forEach(function (k) { attempts[k] = s.attempts[k].slice(); });
    return {
      targets: s.targets.slice(), limit: s.limit, order: s.order, stack: s.stack.slice(),
      status: Object.assign({}, s.status), answers: s.answers.slice(), attempts: attempts,
      seed: s.seed, avoid: s.avoid, mode: s.mode, scope: s.scope ? s.scope.slice() : null
    };
  }

  /* ---- seeded PRNG: same (seed, topic, attempt) always gives the same number, so sessions replay exactly ---- */
  function hashStr(str) {
    let h = 2166136261 >>> 0;
    for (let i = 0; i < str.length; i++) { h ^= str.charCodeAt(i); h = Math.imul(h, 16777619) >>> 0; }
    return h >>> 0;
  }

  function mulberry32(a) {
    return function () {
      a = (a + 0x6D2B79F5) | 0;
      let t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }

  function rand01(seed, key) {
    const f = mulberry32(hashStr(String(seed) + '|' + key));
    f();
    return f();
  }

  const rankOf = function (q) { return DIFF_RANK[q.difficulty] == null ? 1 : DIFF_RANK[q.difficulty]; };

  /**
   * Pick question number `attempt` (1 or 2) for topic id.
   *  - never repeat a question within a session;
   *  - 1st: prefer questions not seen before (session.avoid), avoid advanced when possible;
   *  - 2nd: same level or easier - basic first, then the 1st question's level, then any easier, harder only as a last resort;
   *  - within a tier, the seeded PRNG chooses.
   */
  function pickQuestion(graph, session, id, attempt) {
    const all = graph.bank[id] || [];
    const tried = (session.attempts[id] || []).map(function (a) { return a.qid; });
    const pool = all.filter(function (q) { return tried.indexOf(q.id) < 0; });
    if (!pool.length) return null;
    const avoid = new Set(session.avoid || []);
    const freshFirst = function (list) {
      const f = list.filter(function (q) { return !avoid.has(q.id); });
      return f.length ? f : list;
    };
    let cand;
    if (attempt <= 1) {
      cand = freshFirst(pool);
      const nonAdv = cand.filter(function (q) { return rankOf(q) < 2; });
      if (nonAdv.length) cand = nonAdv;
    } else {
      const first = all.find(function (q) { return q.id === tried[0]; });
      const r0 = first ? rankOf(first) : 1;
      const tiers = [
        pool.filter(function (q) { return rankOf(q) === 0; }),
        pool.filter(function (q) { return rankOf(q) === r0; }),
        pool.filter(function (q) { return rankOf(q) < r0; })
      ];
      const hit = tiers.find(function (t) { return t.length; });
      if (hit) cand = freshFirst(hit);
      else {
        const lo = Math.min.apply(null, pool.map(rankOf));
        cand = freshFirst(pool.filter(function (q) { return rankOf(q) === lo; }));
      }
    }
    const idx = Math.min(cand.length - 1, Math.floor(rand01(session.seed, id + '|' + attempt) * cand.length));
    return cand[idx];
  }

  /**
   * Record an answer to the question nextItem gave.
   *  - 1st correct: topic and all undecided ancestors become mastered (ancestors 'inferred');
   *  - 1st wrong/skip: no verdict yet, ask a 2nd question (weak at once if none is left);
   *  - 2nd correct: shaky, no backtracking;
   *  - 2nd wrong/skip: weak, and its prerequisites (hard first) go on top of the stack.
   * Direct verdicts are never overwritten by inferred ones. extra.text is the typed answer (log only).
   */
  function applyAnswer(graph, session, id, result, extra) {
    if (!RESULTS[result]) throw new Error('Result must be correct / wrong / skip');
    if (!graph.byId[id]) throw new Error('Unknown topic: ' + id);
    const s = cloneSession(session);
    if (s.status[id]) { delete s.status[id]; s.attempts[id] = []; } // answering a decided topic again restarts it
    const prev = s.attempts[id] || [];
    const q = pickQuestion(graph, s, id, prev.length + 1);
    const rec = { id: id, qid: q ? q.id : null, result: result };
    if (extra && extra.text != null && extra.text !== '') rec.text = String(extra.text);
    s.answers.push(rec);
    s.attempts[id] = prev.concat([{ qid: rec.qid, result: result }]);
    const nth = s.attempts[id].length;
    if (result === 'correct') {
      if (nth === 1) {
        s.status[id] = { s: 'mastered', src: 'direct' };
        ancestorSet(graph, id).forEach(function (a) {
          if (!s.status[a]) s.status[a] = { s: 'mastered', src: 'inferred' };
        });
      } else {
        s.status[id] = { s: 'shaky', src: 'direct' };
      }
    } else if (nth === 1 && pickQuestion(graph, s, id, 2)) {
      // first question missed: wait for the second
    } else {
      s.status[id] = { s: 'weak', src: 'direct' };
      const scope = s.scope ? new Set(s.scope) : null;
      const push = graph.prereqs[id]
        .map(function (p) { return p.id; })
        .filter(function (p) { return isTestable(graph, p) && !s.status[p] && (!scope || scope.has(p)); });
      const pushed = new Set(push);
      s.stack = push.concat(s.stack.filter(function (x) { return !pushed.has(x); }));
    }
    return s;
  }

  function nextQuestion(graph, session) {
    if (session.answers.length >= session.limit) return null;
    for (let i = 0; i < session.stack.length; i++) {
      const id = session.stack[i];
      if (!session.status[id] && isTestable(graph, id)) return id;
    }
    return null;
  }

  function nextItem(graph, session) {
    const id = nextQuestion(graph, session);
    if (!id) return null;
    const attempt = (session.attempts[id] || []).length + 1;
    const q = pickQuestion(graph, session, id, attempt);
    return q ? { topicId: id, question: q, attempt: attempt } : null;
  }

  /** Rebuild a session from its answer log (restore, undo, correction). */
  function replay(graph, targets, answers, opts) {
    let s = createSession(graph, targets, opts);
    answers.forEach(function (a) { s = applyAnswer(graph, s, a.id, a.result, { text: a.text }); });
    return s;
  }

  /** mastered / shaky / weak / unknown. A topic with one wrong answer when the cap was hit counts as weak (isUnconfirmed). */
  function statusOf(session, id) {
    const st = session.status[id];
    if (st) return st.s;
    return isUnconfirmed(session, id) ? 'weak' : 'unknown';
  }

  /** First answer wrong but the question cap was reached before a second. */
  function isUnconfirmed(session, id) {
    const a = session.attempts[id];
    return !session.status[id] && !!a && a.length === 1 && a[0].result !== 'correct';
  }

  /* ------------------------------------------------------------------ results */

  function summarize(graph, session) {
    const nodes = session.order;
    const st = function (id) { return statusOf(session, id); };
    const mastered = nodes.filter(function (id) { return st(id) === 'mastered'; });
    const shaky = nodes.filter(function (id) { return st(id) === 'shaky'; });
    const weak = nodes.filter(function (id) { return st(id) === 'weak'; });
    const unconfirmed = weak.filter(function (id) { return isUnconfirmed(session, id); });
    const untested = nodes.filter(function (id) { return st(id) === 'unknown'; });
    const scope = session.scope ? new Set(session.scope) : null;
    const inScope = function (id) { return !scope || scope.has(id); };

    const roots = weak.filter(function (id) {
      return !graph.prereqs[id].some(function (p) { return st(p.id) === 'weak'; });
    }).map(function (id) {
      const unk = graph.prereqs[id].filter(function (p) { return st(p.id) === 'unknown'; });
      const testableUnk = unk.filter(function (p) { return isTestable(graph, p.id); });
      return {
        id: id,
        // untested prerequisites (cap reached): the real root cause may be further back
        pendingPrereqs: testableUnk.filter(function (p) { return inScope(p.id); }).map(function (p) { return p.id; }),
        // screening mode: prerequisites outside the chosen scope, not checked
        outOfScopePrereqs: testableUnk.filter(function (p) { return !inScope(p.id); }).map(function (p) { return p.id; }),
        // prerequisites with no questions
        externalPrereqs: unk.filter(function (p) { return !isTestable(graph, p.id); }).map(function (p) { return p.id; })
      };
    });

    // learning path: roots and shaky topics plus everything after them in the subgraph, minus mastered
    const inSub = new Set(nodes);
    const reach = new Set();
    const queue = roots.map(function (r) { return r.id; }).concat(shaky);
    queue.forEach(function (id) { reach.add(id); });
    while (queue.length) {
      const id = queue.shift();
      graph.dependents[id].forEach(function (d) {
        if (inSub.has(d.id) && !reach.has(d.id)) { reach.add(d.id); queue.push(d.id); }
      });
    }
    const rootSet = new Set(roots.map(function (r) { return r.id; }));
    const targetSet = new Set(scope ? [] : session.targets); // in screening mode every topic is a target, so none is marked
    const topoPos = Object.create(null);
    nodes.forEach(function (id, i) { topoPos[id] = i; });
    const path = nodes.filter(function (id) { return reach.has(id) && st(id) !== 'mastered'; })
      .map(function (id) {
        return { id: id, status: st(id), isRoot: rootSet.has(id), isTarget: targetSet.has(id) };
      });
    // order the path by level (Year 9 -> Unit 4), keeping topological order within a level
    path.sort(function (a, b) {
      return gradeRank(graph, a.id) - gradeRank(graph, b.id) || topoPos[a.id] - topoPos[b.id];
    });

    const pending = session.stack.filter(function (id) { return !session.status[id] && isTestable(graph, id); });
    const next = nextQuestion(graph, session);
    return {
      mode: session.mode || 'target',
      targets: session.targets.slice(),
      asked: session.answers.length,
      limit: session.limit,
      finished: next === null,
      limitReached: session.answers.length >= session.limit && pending.length > 0,
      mastered: mastered, shaky: shaky, weak: weak, unconfirmed: unconfirmed, untested: untested,
      roots: roots, path: path
    };
  }

  /* ------------------------------------------------------------------ path diagram layout */

  /**
   * Nodes: learning path + targets + root causes + every topic asked.
   * Edges: transitive reduction of reachability on those nodes; non-direct edges get direct:false (dotted).
   * Layers run top (prerequisites) to bottom (targets).
   */
  function layout(graph, session, summary) {
    const S = new Set();
    const screen = !!session.scope;
    summary.path.forEach(function (p) { S.add(p.id); });
    if (!screen) session.targets.forEach(function (id) { S.add(id); });
    summary.roots.forEach(function (r) { S.add(r.id); });
    session.answers.forEach(function (a) { S.add(a.id); });
    if (S.size < 3 && !screen) {
      session.targets.forEach(function (id) {
        graph.prereqs[id].slice(0, 6).forEach(function (p) { S.add(p.id); });
      });
    }
    const ids = topoSort(graph, S);
    const edges = [];
    ids.forEach(function (b) {
      const anc = ancestorSet(graph, b);
      ids.forEach(function (a) {
        if (a === b || !anc.has(a)) return;
        const between = ids.some(function (c) {
          return c !== a && c !== b && anc.has(c) && ancestorSet(graph, c).has(a);
        });
        if (between) return;
        const direct = graph.prereqs[b].find(function (p) { return p.id === a; });
        edges.push({ from: a, to: b, direct: !!direct, strength: direct ? direct.strength : 'hard' });
      });
    });
    const layer = Object.create(null);
    ids.forEach(function (id) {
      let l = 0;
      edges.forEach(function (e) { if (e.to === id) l = Math.max(l, layer[e.from] + 1); });
      layer[id] = l;
    });
    const nLayers = ids.reduce(function (m, id) { return Math.max(m, layer[id] + 1); }, 1);
    const rows = [];
    for (let i = 0; i < nLayers; i++) rows.push([]);
    ids.forEach(function (id) { rows[layer[id]].push(id); });
    // barycentre ordering to reduce crossings
    const slot = Object.create(null);
    rows.forEach(function (r) { r.forEach(function (id, i) { slot[id] = i; }); });
    const bary = function (id, nbrs) {
      if (!nbrs.length) return slot[id];
      return nbrs.reduce(function (s, n) { return s + slot[n]; }, 0) / nbrs.length;
    };
    for (let it = 0; it < 4; it++) {
      for (let l = 1; l < nLayers; l++) {
        rows[l].sort(function (a, b) {
          return bary(a, edges.filter(function (e) { return e.to === a; }).map(function (e) { return e.from; })) -
                 bary(b, edges.filter(function (e) { return e.to === b; }).map(function (e) { return e.from; }));
        });
        rows[l].forEach(function (id, i) { slot[id] = i; });
      }
      for (let l = nLayers - 2; l >= 0; l--) {
        rows[l].sort(function (a, b) {
          return bary(a, edges.filter(function (e) { return e.from === a; }).map(function (e) { return e.to; })) -
                 bary(b, edges.filter(function (e) { return e.from === b; }).map(function (e) { return e.to; }));
        });
        rows[l].forEach(function (id, i) { slot[id] = i; });
      }
    }
    const rootSet = new Set(summary.roots.map(function (r) { return r.id; }));
    const targetSet = new Set(screen ? [] : session.targets);
    const nodes = [];
    rows.forEach(function (r, l) {
      r.forEach(function (id, i) {
        nodes.push({
          id: id, layer: l, col: i, cols: r.length,
          status: statusOf(session, id), isTarget: targetSet.has(id), isRoot: rootSet.has(id)
        });
      });
    });
    return { nodes: nodes, edges: edges, layers: nLayers, maxCols: rows.reduce(function (m, r) { return Math.max(m, r.length); }, 1) };
  }

  /* ------------------------------------------------------------------ levels and chapters */

  // Year 9 < Year 10 < Year 10 optional < Unit 1 < ... < Unit 4 (same order as scripts/qlib.py rank_of)
  const BAND_RANK = { y9: 0, y10: 1, y10opt: 2 };
  const SENIOR = { general: 1, methods: 1, specialist: 1 };

  /** Rank used to order the learning path. Hand-made graphs without a band rank 0. */
  function gradeRank(graph, id) {
    const t = graph.byId[id];
    if (!t || !t.band) return 0;
    if (SENIOR[t.band]) return 2 + (t.unit || 0);
    return BAND_RANK[t.band] == null ? 0 : BAND_RANK[t.band];
  }

  /**
   * "Year 10 · Algebra"                             -> {volume:'Year 10', chapterNo:'', chapterName:'Algebra'}
   * "Methods U1 · T1 Surds and quadratic functions" -> {volume:'Methods U1', chapterNo:'T1', chapterName:'Surds and quadratic functions'}
   */
  function parseChapter(chapter) {
    const s = chapter || '';
    const k = s.indexOf(' · ');
    if (k < 0) return { volume: '', chapterNo: '', chapterName: s, section: '' };
    const volume = s.slice(0, k);
    const rest = s.slice(k + 3);
    const m = /^(T\d+) (.+)$/.exec(rest);
    return m ? { volume: volume, chapterNo: m[1], chapterName: m[2], section: '' }
      : { volume: volume, chapterNo: '', chapterName: rest, section: '' };
  }

  /** Single subject in this fork; kept for API compatibility. */
  function subjectOf() { return 'math'; }

  /**
   * Topics in a whole year, band or unit: 'Year 9', 'Year 10', 'Year 10 Optional', 'Methods' (all units),
   * 'Methods U1', 'General U3' ... Case-insensitive. Returns {ids, volumes, label} or null.
   */
  function gradeTargets(graph, scope) {
    const key = String(scope == null ? '' : scope).trim().toLowerCase().replace(/\s+/g, ' ');
    if (!key) return null;
    const volumes = [];
    graph.topics.forEach(function (t) {
      const v = parseChapter(t.chapter).volume;
      const vl = v.toLowerCase();
      if ((vl === key || vl.indexOf(key + ' u') === 0) && volumes.indexOf(v) < 0) volumes.push(v);
    });
    if (!volumes.length) return null;
    const ids = graph.topics.filter(function (t) {
      return !t.external && volumes.indexOf(parseChapter(t.chapter).volume) >= 0;
    }).map(function (t) { return t.id; });
    return ids.length ? { ids: ids, volumes: volumes, label: volumes.length === 1 ? volumes[0] : String(scope).trim() } : null;
  }

  /** Per-chapter counts of mastered / shaky / weak / untested; chapters with most weak topics first. */
  function chapterSummary(graph, session) {
    const inOrder = new Set(session.order);
    const byKey = Object.create(null);
    const list = [];
    graph.topics.forEach(function (t) {
      if (t.external || !inOrder.has(t.id)) return;
      const c = parseChapter(t.chapter);
      const key = c.volume + ' ' + c.chapterNo + ' ' + c.chapterName;
      let ch = byKey[key];
      if (!ch) {
        ch = byKey[key] = {
          key: key, volume: c.volume, chapterNo: c.chapterNo, chapterName: c.chapterName,
          label: (c.volume ? c.volume + ' ' : '') + c.chapterNo + ' ' + c.chapterName,
          total: 0, mastered: 0, shaky: 0, weak: 0, untested: 0, weakIds: [], shakyIds: [], untestedIds: [], _i: list.length
        };
        list.push(ch);
      }
      const st = statusOf(session, t.id);
      ch.total++;
      if (st === 'mastered') ch.mastered++;
      else if (st === 'shaky') { ch.shaky++; ch.shakyIds.push(t.id); }
      else if (st === 'weak') { ch.weak++; ch.weakIds.push(t.id); }
      else { ch.untested++; ch.untestedIds.push(t.id); }
    });
    list.sort(function (a, b) { return b.weak - a.weak || b.shaky - a.shaky || a._i - b._i; });
    list.forEach(function (ch) { delete ch._i; });
    return list;
  }

  /** Expand ids from the URL through data/id-aliases.json ({old: {targets: [...]}} or {old: [...]}). Unknown ids pass through. */
  function resolveTargets(rawIds, aliases) {
    const map = aliases || {};
    const out = [];
    const seen = Object.create(null);
    (Array.isArray(rawIds) ? rawIds : [rawIds]).forEach(function (id) {
      if (!id) return;
      let targets = null;
      const spec = map[id];
      if (spec && Array.isArray(spec.targets)) targets = spec.targets;
      else if (Array.isArray(spec)) targets = spec;
      const list = targets && targets.length ? targets : [id];
      list.forEach(function (tid) {
        if (!seen[tid]) { seen[tid] = true; out.push(tid); }
      });
    });
    return out;
  }

  /* ------------------------------------------------------------------ answer judging */
  // Gives 'correct' / 'wrong' only when sure; otherwise 'manual' (the student compares with the worked answer).

  function normalizeText(input) {
    let s = String(input == null ? '' : input);
    s = s.replace(/²/g, '^2').replace(/³/g, '^3').replace(/[º˚∘]/g, '°');
    s = s.normalize('NFKC');
    s = s.replace(/[−‐-―﹣]/g, '-')
      .replace(/[“”‘’]/g, '"')
      .replace(/[×·⋅∙]/g, '*')
      .replace(/÷/g, '/')
      .replace(/<=/g, '≤').replace(/>=/g, '≥')
      .replace(/[\[\]{}]/g, function (c) { return c === '[' || c === '{' ? '(' : ')'; });
    s = s.replace(/\s+(and|or)\s+/gi, ',');                       // "2 and -3" -> "2,-3"
    s = s.replace(/(\d)\s*(degrees?|deg)\b/gi, '$1°');
    s = s.replace(/(\d)\s+(\d+\s*\/\s*\d+)/g, '$1&$2');  // mixed number "1 1/2" -> "1&1/2"
    s = s.replace(/\s+/g, '').toLowerCase();
    s = s.replace(/^(answer|ans)[:=]/, '');
    s = s.replace(/^\$(?=[\d.])/, '').replace(/^-\$(?=[\d.])/, '-');  // $200 -> 200
    s = s.replace(/[.!]+$/, '');
    if (/^[+-]?\d{1,3}(,\d{3})+(\.\d+)?$/.test(s)) s = s.replace(/,/g, ''); // thousands separators
    return s;
  }

  function splitTop(s, seps) {
    const parts = [];
    let depth = 0;
    let cur = '';
    for (let i = 0; i < s.length; i++) {
      const c = s[i];
      if (c === '(') depth++;
      else if (c === ')') depth = Math.max(0, depth - 1);
      if (depth === 0 && seps.indexOf(c) >= 0) { parts.push(cur); cur = ''; } else cur += c;
    }
    parts.push(cur);
    return parts.filter(function (p) { return p !== ''; });
  }

  function gcd(a, b) { a = a < 0n ? -a : a; b = b < 0n ? -b : b; while (b) { const t = a % b; a = b; b = t; } return a; }

  function ratio(n, d) {
    if (d === 0n) return null;
    if (d < 0n) { n = -n; d = -d; }
    const g = gcd(n, d) || 1n;
    return [n / g, d / g];
  }

  function decToRatio(str) {
    const i = str.indexOf('.');
    if (i < 0) return ratio(BigInt(str), 1n);
    const frac = str.slice(i + 1);
    const whole = str.slice(0, i) || '0';
    return ratio(BigInt(whole + frac), 10n ** BigInt(frac.length));
  }

  function isWrapped(t) {
    if (t[0] !== '(' || t[t.length - 1] !== ')') return false;
    let depth = 0;
    for (let i = 0; i < t.length; i++) {
      if (t[i] === '(') depth++;
      else if (t[i] === ')') { depth--; if (depth === 0 && i < t.length - 1) return false; }
    }
    return depth === 0;
  }

  const UNIT_ALIASES = {
    'm': 'm', 'metre': 'm', 'metres': 'm', 'cm': 'cm', 'mm': 'mm', 'km': 'km',
    'kg': 'kg', 'g': 'g', 's': 's', 'sec': 's', 'seconds': 's', 'min': 'min', 'h': 'h', 'hr': 'h', 'hours': 'h',
    'm^2': 'm^2', 'm2': 'm^2', 'sqm': 'm^2', 'cm^2': 'cm^2', 'cm2': 'cm^2', 'km^2': 'km^2', 'ha': 'ha',
    'm^3': 'm^3', 'm3': 'm^3', 'cm^3': 'cm^3', 'cm3': 'cm^3', 'l': 'L', 'ml': 'mL',
    'm/s': 'm/s', 'km/h': 'km/h', '°': '°', 'units': '', 'unit': ''
  };

  function canonUnit(u) {
    if (!u) return { name: '', known: true };
    if (UNIT_ALIASES[u] != null) return { name: UNIT_ALIASES[u], known: true };
    if (/^[a-z]{3,12}$/.test(u)) return { name: u, known: false }; // a word we don't know: let the student self-check
    return null; // not a unit, so this is not "number + unit"
  }

  /** Integer, decimal, fraction a/b, mixed number, percentage, signs and brackets; optional trailing unit. */
  function parseNumeric(str) {
    let t = str;
    let neg = false;
    for (let guard = 0; guard < 4; guard++) {
      if (isWrapped(t)) { t = t.slice(1, -1); continue; }
      if ((t[0] === '-' || t[0] === '+') && isWrapped(t.slice(1))) { if (t[0] === '-') neg = !neg; t = t.slice(2, -1); continue; }
      break;
    }
    const m = /^([+-]?)(?:(\d+)&)?(\d+(?:\.\d+)?|\.\d+)(?:\/(\d+(?:\.\d+)?|\.\d+))?(%|°)?(.*)$/.exec(t);
    if (!m) return null;
    const whole = m[2], numS = m[3], denS = m[4], mark = m[5];
    const rest = m[6];
    if (whole && !denS) return null;
    let val;
    if (whole) {
      const n = decToRatio(numS), d = decToRatio(denS);
      if (!n || !d || d[0] === 0n) return null;
      const f = ratio(n[0] * d[1], n[1] * d[0]);
      const w = ratio(BigInt(whole), 1n);
      val = ratio(w[0] * f[1] + f[0], f[1]);
    } else if (denS) {
      const n = decToRatio(numS), d = decToRatio(denS);
      if (!n || !d || d[0] === 0n) return null;
      val = ratio(n[0] * d[1], n[1] * d[0]);
    } else {
      val = decToRatio(numS);
    }
    if (!val) return null;
    if (m[1] === '-') neg = !neg;
    let n = neg ? -val[0] : val[0];
    let d = val[1];
    let unit = { name: '', known: true };
    if (mark === '%') {
      const r = ratio(n, d * 100n);
      n = r[0]; d = r[1];
      if (rest) return null;
    } else if (mark === '°') {
      unit = { name: '°', known: true };
      if (rest) return null;
    } else if (rest) {
      unit = canonUnit(rest);
      if (!unit) return null;
    }
    return { key: n + '/' + d, unit: unit };
  }

  function analyzePart(p) {
    let variable = '';
    let body = p;
    const m = /^([a-z](?:\([a-z]\))?)=(.+)$/.exec(p);
    if (m) { variable = m[1]; body = m[2]; }
    const num = parseNumeric(body);
    if (num) return { raw: p, variable: variable, kind: 'num', key: num.key, unit: num.unit };
    const tm = /^\((.+)\)$/.exec(body);
    if (tm) {
      const items = splitTop(tm[1], ',');
      const nums = items.map(parseNumeric);
      if (items.length > 1 && nums.every(Boolean)) {
        return { raw: p, variable: variable, kind: 'tuple', key: 't:' + nums.map(function (x) { return x.key; }).join(','), unit: { name: '', known: true } };
      }
    }
    return { raw: p, variable: variable, kind: 'text', key: body, unit: { name: '', known: true } };
  }

  function parseAnswer(input) {
    const norm = normalizeText(input);
    const parts = splitTop(norm, ',;').map(analyzePart);
    return { norm: norm, parts: parts };
  }

  // 'eq' | 'ne' | 'unsure'
  function partCompare(a, b) {
    if (a.kind !== b.kind || a.key !== b.key) return 'ne';
    const ua = a.unit, ub = b.unit;
    if (!ua.name || !ub.name || ua.name === ub.name) return 'eq';
    return ua.known && ub.known ? 'ne' : 'unsure';
  }

  function sameMultiset(as, bs, ignoreVar) {
    if (as.length !== bs.length) return null;
    const left = bs.slice();
    let fuzzy = false;
    for (let i = 0; i < as.length; i++) {
      let hit = -1;
      for (let j = 0; j < left.length; j++) {
        if (!ignoreVar && as[i].variable !== left[j].variable) continue;
        const c = partCompare(as[i], left[j]);
        if (c === 'ne') continue;
        if (c === 'unsure') fuzzy = true;
        hit = j;
        break;
      }
      if (hit < 0) return null;
      left.splice(hit, 1);
    }
    return fuzzy ? 'unsure' : 'eq';
  }

  function allNumeric(parts) { return parts.every(function (p) { return p.kind === 'num' || p.kind === 'tuple'; }); }

  function compareParsed(u, r) {
    let res = null;
    if (u.parts.length === r.parts.length) {
      const refVars = r.parts.map(function (p) { return p.variable; });
      const refVarsDistinct = r.parts.length > 1 && refVars.every(Boolean) && new Set(refVars).size === refVars.length;
      if (refVarsDistinct) {
        if (u.parts.every(function (p) { return p.variable; })) res = sameMultiset(u.parts, r.parts, false);
        else if (u.parts.every(function (p) { return !p.variable; })) {
          // no variable names written: match in the reference's order (b then c)
          res = 'eq';
          for (let i = 0; i < u.parts.length; i++) {
            const c = partCompare(u.parts[i], r.parts[i]);
            if (c === 'ne') { res = null; break; }
            if (c === 'unsure') res = 'unsure';
          }
        } else return { relation: 'unsure' };
      } else {
        res = sameMultiset(u.parts, r.parts, true);
      }
    }
    if (res === 'eq') return { relation: 'equal' };
    if (res === 'unsure') return { relation: 'unsure' };
    return { relation: allNumeric(u.parts) && allNumeric(r.parts) ? 'different' : 'unsure' };
  }

  /** Identical or numerically equivalent -> correct; both numeric but different -> wrong; anything else -> manual. */
  function judgeAnswer(user, reference) {
    const u = parseAnswer(user);
    const r = parseAnswer(reference);
    if (!u.norm) return { verdict: 'manual', reason: 'empty' };
    if (u.norm === r.norm) return { verdict: 'correct', reason: 'identical' };
    if (!r.parts.length) return { verdict: 'manual', reason: 'no-reference' };
    const c = compareParsed(u, r);
    if (c.relation === 'equal') return { verdict: 'correct', reason: 'equivalent' };
    if (c.relation === 'different') return { verdict: 'wrong', reason: 'numeric-mismatch' };
    return { verdict: 'manual', reason: 'unsure' };
  }

  const MANUAL_EMPTY = { verdict: 'manual', reason: 'empty' };

  function judgeChoice(user, q) {
    const raw = String(user == null ? '' : user).trim();
    if (!raw) return MANUAL_EMPTY;
    const choices = q.choices || [];
    const keys = choices.map(function (c) { return c.key; });
    let letter = null;
    const m = /^\(?([A-Za-z])[).:]?$/.exec(raw);
    if (m) letter = m[1].toUpperCase();
    else {
      const n = normalizeText(raw);
      const hit = choices.find(function (c) { return normalizeText(c.text) === n; });
      if (hit) letter = hit.key;
    }
    if (!letter || keys.indexOf(letter) < 0) return { verdict: 'manual', reason: 'unrecognized' };
    return letter === q.answer ? { verdict: 'correct', reason: 'choice' } : { verdict: 'wrong', reason: 'choice' };
  }

  function judgeNumeric(user, q) {
    const u = parseAnswer(user);
    if (!u.norm) return MANUAL_EMPTY;
    const refs = [q.answer].concat(q.accept || []);
    for (let i = 0; i < refs.length; i++) {
      if (parseAnswer(refs[i]).norm === u.norm) return { verdict: 'correct', reason: 'identical' };
    }
    const main = parseAnswer(q.answer);
    const named = function (ps) { return ps.every(function (p) { return p.variable; }); };
    if (!q.unordered && main.parts.length > 1 && named(main.parts) && named(u.parts)) {
      // both sides name their variables (b = -2, c = 1): match by name, in any order
      const byName = sameMultiset(u.parts, main.parts, false);
      if (byName === 'eq') return { verdict: 'correct', reason: 'equivalent' };
      if (byName === 'unsure') return { verdict: 'manual', reason: 'unsure' };
      return allNumeric(u.parts) ? { verdict: 'wrong', reason: 'numeric-mismatch' } : { verdict: 'manual', reason: 'unsure' };
    }
    if (!q.unordered && main.parts.length > 1) {
      // several answers in a fixed order: compare position by position (variable names ignored)
      if (u.parts.length !== main.parts.length) {
        return allNumeric(u.parts) ? { verdict: 'wrong', reason: 'count-mismatch' } : { verdict: 'manual', reason: 'unsure' };
      }
      let res = 'eq';
      for (let i = 0; i < u.parts.length; i++) {
        const c = partCompare(u.parts[i], main.parts[i]);
        if (c === 'ne') { res = 'ne'; break; }
        if (c === 'unsure') res = 'unsure';
      }
      if (res === 'eq') return { verdict: 'correct', reason: 'equivalent' };
      if (res === 'ne' && allNumeric(u.parts) && allNumeric(main.parts)) return { verdict: 'wrong', reason: 'numeric-mismatch' };
      return { verdict: 'manual', reason: 'unsure' };
    }
    const r = judgeAnswer(user, q.answer);
    if (r.verdict === 'correct') return r;
    for (let i = 1; i < refs.length; i++) {
      if (judgeAnswer(user, refs[i]).verdict === 'correct') return { verdict: 'correct', reason: 'accept' };
    }
    return r;
  }

  function judgeShort(user, q) {
    const u = normalizeText(user);
    if (!u) return MANUAL_EMPTY;
    const refs = [q.answer].concat(q.accept || []);
    for (let i = 0; i < refs.length; i++) {
      if (normalizeText(refs[i]) === u) return { verdict: 'correct', reason: i ? 'accept' : 'identical' };
    }
    for (let i = 0; i < refs.length; i++) {
      if (judgeAnswer(user, refs[i]).verdict === 'correct') return { verdict: 'correct', reason: 'equivalent' };
    }
    return { verdict: 'manual', reason: 'unsure' };
  }

  /** choice: letter or choice text; numeric: exact rational equivalence; short: normalised match; self: always manual. */
  function judgeQuestion(q, user) {
    switch (q.type) {
      case 'choice': return judgeChoice(user, q);
      case 'numeric': return judgeNumeric(user, q);
      case 'short': return judgeShort(user, q);
      case 'self': return { verdict: 'manual', reason: 'self' };
      default: return judgeAnswer(user, q.answer);
    }
  }

  return {
    DEFAULT_LIMIT: DEFAULT_LIMIT,
    SCREEN_LIMIT: SCREEN_LIMIT,
    gradeTargets: gradeTargets,
    subjectOf: subjectOf,
    chapterSummary: chapterSummary,
    buildGraph: buildGraph,
    questionById: questionById,
    pickQuestion: pickQuestion,
    nextItem: nextItem,
    isUnconfirmed: isUnconfirmed,
    mulberry32: mulberry32,
    judgeQuestion: judgeQuestion,
    ancestors: ancestors,
    topoSort: topoSort,
    subgraph: subgraph,
    isTestable: isTestable,
    createSession: createSession,
    applyAnswer: applyAnswer,
    nextQuestion: nextQuestion,
    replay: replay,
    statusOf: statusOf,
    summarize: summarize,
    layout: layout,
    parseChapter: parseChapter,
    gradeRank: gradeRank,
    resolveTargets: resolveTargets,
    normalizeText: normalizeText,
    judgeAnswer: judgeAnswer
  };
});
