/* Engine tests (Node, no dependencies): node tests/test_engine.js */
'use strict';
const fs = require('fs');
const path = require('path');
const assert = require('assert');
const E = require('../diagnose/engine.js');

let passed = 0;
function test(name, fn) {
  try { fn(); passed++; } catch (e) { console.error('FAIL ' + name + '\n  ' + e.message); process.exitCode = 1; }
}
const load = function (f) { return JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'data', f), 'utf8')); };

/* ---------------- hand-made graph: A <- B <- C (C is the target), A <- D, D soft prereq of C */
function q(topic, n, diff) { return { id: topic + '_q' + n, topicId: topic, difficulty: diff || 'basic', type: 'numeric', prompt: topic + n, answer: '1', explanation: '' }; }
const T = ['A', 'B', 'C', 'D'].map(function (id) { return { id: id, name: id, chapter: 'Year 9 · Algebra', band: 'y9' }; });
const DEPS = [
  { topicId: 'B', prerequisiteId: 'A', strength: 'hard' },
  { topicId: 'C', prerequisiteId: 'B', strength: 'hard' },
  { topicId: 'C', prerequisiteId: 'D', strength: 'soft' }
];
const Q = [].concat.apply([], ['A', 'B', 'C', 'D'].map(function (t) { return [q(t, 1), q(t, 2), q(t, 3, 'standard')]; }));
const g = E.buildGraph(T, DEPS, Q);

function run(plan, targets, opts) {
  let s = E.createSession(g, targets || ['C'], Object.assign({ seed: 't' }, opts));
  for (let it = E.nextItem(g, s), n = 0; it && n < 100; it = E.nextItem(g, s), n++) {
    const seq = plan[it.topicId] || ['correct'];
    s = E.applyAnswer(g, s, it.topicId, seq[Math.min(it.attempt - 1, seq.length - 1)]);
  }
  return s;
}

test('first answer correct masters target and infers ancestors', function () {
  const s = run({});
  const sum = E.summarize(g, s);
  assert.strictEqual(s.answers.length, 1);
  assert.deepStrictEqual(sum.mastered.sort(), ['A', 'B', 'C', 'D']);
  assert.strictEqual(s.status.A.src, 'inferred');
});

test('wrong twice backtracks hard prerequisite before soft', function () {
  const s = run({ C: ['wrong', 'wrong'] });
  assert.deepStrictEqual(s.answers.map(function (a) { return a.id; }), ['C', 'C', 'B', 'D']);
});

test('root cause is the deepest weak topic', function () {
  const s = run({ C: ['wrong'], B: ['wrong'] });
  const sum = E.summarize(g, s);
  assert.deepStrictEqual(sum.roots.map(function (r) { return r.id; }), ['B']);
  assert.deepStrictEqual(sum.path.map(function (p) { return p.id; }), ['B', 'C']);
});

test('shaky does not backtrack and goes on the path', function () {
  const s = run({ C: ['wrong', 'correct'] });
  const sum = E.summarize(g, s);
  assert.deepStrictEqual(sum.shaky, ['C']);
  assert.strictEqual(s.answers.length, 2);
  assert.deepStrictEqual(sum.path.map(function (p) { return p.id; }), ['C']);
});

test('second question is basic and differs from the first', function () {
  let s = E.createSession(g, ['C'], { seed: 'x' });
  const first = E.nextItem(g, s).question.id;
  s = E.applyAnswer(g, s, 'C', 'wrong');
  const second = E.nextItem(g, s).question;
  assert.notStrictEqual(second.id, first);
  assert.strictEqual(second.difficulty, 'basic');
});

test('question limit marks unconfirmed topic as weak', function () {
  const s = run({ C: ['wrong'] }, ['C'], { limit: 1 });
  const sum = E.summarize(g, s);
  assert.ok(sum.limitReached);
  assert.deepStrictEqual(sum.unconfirmed, ['C']);
});

test('replay reproduces a session exactly', function () {
  const s = run({ C: ['wrong', 'wrong'], B: ['wrong', 'correct'] });
  const r = E.replay(g, ['C'], s.answers, { seed: 't' });
  assert.deepStrictEqual(r.status, s.status);
  assert.deepStrictEqual(r.answers, s.answers);
});

test('screening never leaves the scope', function () {
  const s = run({ C: ['wrong', 'wrong'], B: ['wrong', 'wrong'] }, ['B', 'C'], { mode: 'screen' });
  s.answers.forEach(function (a) { assert.ok(['B', 'C'].indexOf(a.id) >= 0, a.id); });
  const sum = E.summarize(g, s);
  assert.deepStrictEqual(sum.roots[0].outOfScopePrereqs, ['A']);
});

/* ---------------- consistent simulated students on the real data */
const topics = load('topics.json');
const deps = load('dependencies.json');
const questions = load('questions.json');
const G = E.buildGraph(topics, deps, questions);

test('real data: graph builds and is acyclic', function () {
  assert.ok(topics.length >= 30);
  E.topoSort(G, topics.map(function (t) { return t.id; }));
});

test('real data: a consistent student gets the expected root cause', function () {
  // The student knows everything except topic X and everything that depends on X.
  const target = 'qm_m1_007';
  const sub = E.subgraph(G, [target]).nodes;
  let checked = 0;
  sub.forEach(function (x) {
    if (x === target) return;
    const bad = new Set([x]);
    sub.forEach(function (id) { if (E.ancestors(G, id).has(x)) bad.add(id); });
    let s = E.createSession(G, [target], { seed: 'c', limit: 200 });
    for (let it = E.nextItem(G, s); it; it = E.nextItem(G, s)) {
      s = E.applyAnswer(G, s, it.topicId, bad.has(it.topicId) ? 'wrong' : 'correct');
    }
    const sum = E.summarize(G, s);
    assert.deepStrictEqual(sum.roots.map(function (r) { return r.id; }), [x], 'missing ' + x);
    sum.path.forEach(function (p) { assert.ok(bad.has(p.id), p.id + ' should not be on the path'); });
    checked++;
  });
  assert.ok(checked > 10);
});

test('real data: learning path is ordered by level', function () {
  let s = E.createSession(G, ['qm_m1_007'], { seed: 'p', limit: 200 });
  for (let it = E.nextItem(G, s); it; it = E.nextItem(G, s)) s = E.applyAnswer(G, s, it.topicId, 'wrong');
  const ranks = E.summarize(G, s).path.map(function (p) { return E.gradeRank(G, p.id); });
  assert.deepStrictEqual(ranks, ranks.slice().sort(function (a, b) { return a - b; }));
  assert.strictEqual(ranks[0], 0);
});

test('real data: every keyed answer is judged correct', function () {
  questions.forEach(function (qq) {
    const v = E.judgeQuestion(qq, qq.answer).verdict;
    assert.strictEqual(v, 'correct', qq.id + ' -> ' + v);
  });
});

test('gradeTargets understands levels and units', function () {
  assert.strictEqual(E.gradeTargets(G, 'Year 9').ids.length, topics.filter(function (t) { return t.band === 'y9'; }).length);
  assert.strictEqual(E.gradeTargets(G, 'methods').label, 'Methods U1');
  assert.strictEqual(E.gradeTargets(G, 'Specialist U4'), null);
});

/* ---------------- judging */
test('judging: numbers, fractions, units, order', function () {
  const J = function (ans, user, extra) { return E.judgeQuestion(Object.assign({ type: 'numeric', answer: ans }, extra), user).verdict; };
  assert.strictEqual(J('1/2', '0.5'), 'correct');
  assert.strictEqual(J('1/3', '0.333'), 'wrong');
  assert.strictEqual(J('200', '$200'), 'correct');
  assert.strictEqual(J('200', '200 m²'), 'correct');
  assert.strictEqual(J('3, -5', '-5 and 3', { unordered: true }), 'correct');
  assert.strictEqual(J('3, -5', 'x = -5 or x = 3', { unordered: true }), 'correct');
  assert.strictEqual(J('(2, -5)', '(2,-5)'), 'correct');
  assert.strictEqual(J('(2, -5)', '(-5, 2)'), 'wrong');
  assert.strictEqual(J('b=-2, c=1', 'c = 1, b = -2'), 'correct');
  assert.strictEqual(J('b=-2, c=1', '1, -2'), 'wrong');
  assert.strictEqual(J('5', 'x+5'), 'manual');
  assert.strictEqual(E.judgeQuestion({ type: 'choice', answer: 'B', choices: [{ key: 'A', text: 'x' }, { key: 'B', text: 'y' }] }, 'b').verdict, 'correct');
});

console.log(passed + ' tests passed' + (process.exitCode ? ', some FAILED' : ''));
