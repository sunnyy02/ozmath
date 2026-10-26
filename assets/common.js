/* Shared helpers for home, explore and diagnose (no build step, no dependencies). window.QM */
(function () {
  'use strict';

  const BANDS = [
    { id: 'y9', label: 'Year 9', blurb: 'Australian Curriculum v9.0, Year 9' },
    { id: 'y10', label: 'Year 10', blurb: 'Australian Curriculum v9.0, Year 10' },
    { id: 'y10opt', label: 'Year 10 Optional', blurb: 'Optional content for post-Year 10 pathways' },
    { id: 'general', label: 'General', blurb: 'QCAA General Mathematics 2025, Units 1–4' },
    { id: 'methods', label: 'Methods', blurb: 'QCAA Mathematical Methods 2025, Units 1–4' },
    { id: 'specialist', label: 'Specialist', blurb: 'QCAA Specialist Mathematics 2025, Units 1–4' }
  ];
  const BAND_LABEL = {};
  BANDS.forEach(function (b) { BAND_LABEL[b.id] = b.label; });
  const BAND_VAR = { y9: 'y9', y10: 'y10', y10opt: 'opt', general: 'gen', methods: 'mm', specialist: 'sm' };

  function h(tag, attrs) {
    const el = document.createElement(tag);
    if (attrs) {
      Object.keys(attrs).forEach(function (k) {
        const v = attrs[k];
        if (v == null || v === false) return;
        if (k === 'text') el.textContent = v;
        else if (k === 'class') el.className = v;
        else if (k.slice(0, 2) === 'on' && typeof v === 'function') el.addEventListener(k.slice(2), v);
        else el.setAttribute(k, v === true ? '' : v);
      });
    }
    for (let i = 2; i < arguments.length; i++) append(el, arguments[i]);
    return el;
  }
  function append(el, c) {
    if (c == null || c === false) return;
    if (Array.isArray(c)) { c.forEach(function (x) { append(el, x); }); return; }
    el.append(c instanceof Node ? c : document.createTextNode(String(c)));
  }

  function fetchJson(url) {
    return fetch(url).then(function (r) {
      if (!r.ok) throw new Error(url + ': HTTP ' + r.status);
      return r.json();
    });
  }

  /** Loads data/*.json relative to `base` ('./' or '../'). Questions and aliases are optional. */
  function loadData(base) {
    const opt = function (p) { return fetchJson(base + p).catch(function () { return null; }); };
    return Promise.all([
      fetchJson(base + 'data/topics.json'), fetchJson(base + 'data/dependencies.json'),
      fetchJson(base + 'data/standards.json'), opt('data/questions.json'), opt('data/id-aliases.json')
    ]).then(function (r) {
      const std = {};
      r[2].forEach(function (s) { std[s.id] = s; });
      return { topics: r[0], deps: r[1], standards: r[2], stdById: std, questions: r[3] || [], aliases: r[4] || {} };
    });
  }

  function volumeOf(t) { const k = (t.chapter || '').indexOf(' · '); return k < 0 ? t.chapter : t.chapter.slice(0, k); }
  function groupOf(t) { const k = (t.chapter || '').indexOf(' · '); return k < 0 ? '' : t.chapter.slice(k + 3); }
  function bandTag(t) { return h('span', { class: 'tag ' + t.band, text: volumeOf(t) }); }

  function cssVar(name) { return getComputedStyle(document.documentElement).getPropertyValue(name).trim(); }
  function bandColors(band) {
    const v = BAND_VAR[band] || 'y9';
    return { fg: cssVar('--band-' + v), bg: cssVar('--band-' + v + '-bg') };
  }

  function lsGet(k) { try { return JSON.parse(localStorage.getItem(k)); } catch (e) { return null; } }
  function lsSet(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) { /* private mode */ } }
  function lsDel(k) { try { localStorage.removeItem(k); } catch (e) { /* ignore */ } }

  function clip(name, n) { return name.length > n ? name.slice(0, n - 1) + '…' : name; }

  window.QM = {
    BANDS: BANDS, BAND_LABEL: BAND_LABEL, h: h, append: append, loadData: loadData,
    volumeOf: volumeOf, groupOf: groupOf, bandTag: bandTag, cssVar: cssVar, bandColors: bandColors,
    lsGet: lsGet, lsSet: lsSet, lsDel: lsDel, clip: clip
  };
})();
