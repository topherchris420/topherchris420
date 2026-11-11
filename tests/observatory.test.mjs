import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { test } from "node:test";
import { JSDOM, VirtualConsole } from "jsdom";

const html = readFileSync(new URL("../docs/observatory.html", import.meta.url), "utf8");
const sourceLedger = JSON.parse(readFileSync(new URL("../experiments/ledger.json", import.meta.url), "utf8"));
const sourceAtlas = JSON.parse(readFileSync(new URL("../docs/atlas.json", import.meta.url), "utf8"));
const currentCount = sourceAtlas.projects.filter(p => !["archived", "fork"].includes(p.status)).length;
const totalCount = sourceAtlas.projects.length;

function page(hash = "") {
  const errors = [];
  const downloads = [];
  const console = new VirtualConsole();
  console.on("jsdomError", error => errors.push(error));
  const dom = new JSDOM(html, {
    url: `https://observatory.example/${hash}`, runScripts: "dangerously", virtualConsole: console,
    // JSDOM supplies a DOM, not a layout engine. Stub only platform APIs it lacks.
    beforeParse(window) {
      window.matchMedia = () => ({matches: false, addEventListener() {}});
      window.HTMLElement.prototype.scrollIntoView = function () {};
      window.URL.createObjectURL = blob => { downloads.push(blob); return "blob:export"; };
      window.URL.revokeObjectURL = () => {};
      window.HTMLAnchorElement.prototype.click = function () {};
      window.print = () => {};
    },
  });
  const {window} = dom;
  const doc = window.document;
  const get = id => doc.getElementById(id);
  const visible = () => [...doc.querySelectorAll(".record:not([hidden])")].map(node => node.id);
  const set = (id, value) => {
    const node = get(id);
    if (node.type === "checkbox") node.checked = value; else node.value = value;
    node.dispatchEvent(new window.Event("input", {bubbles: true}));
  };
  const select = id => doc.querySelector(`.compare-control input[value="${id}"]`).click();
  const close = () => { assert.deepEqual(errors, []); window.close(); };
  return {dom, window, doc, get, visible, set, select, close, errors, downloads};
}

test("initial display hides archives, preserves review dates and shows real inventory", () => {
  const p = page();
  assert.equal(p.visible().length, currentCount);
  assert(p.get("result-count").textContent.startsWith(`${currentCount} of ${totalCount}`));
  assert.match(p.get("humantouch").textContent, /2026-10-04/);
  assert.match(p.doc.querySelector(".field-note").textContent, /2026-11-10/);
  assert.equal(p.get("filters").hidden, false);
  p.close();
});

test("exact state filters retain supported and failed scopes on the same record", () => {
  const p = page();
  p.set("state", "SUPPORTED");
  const expected = sourceLedger.experiments.filter(e => e.state.some(s => s.state === "SUPPORTED")).map(e => e.id).sort();
  assert.deepEqual(p.visible().sort(), expected);
  assert.match(p.get("qnp").textContent, /NOT SUPPORTED/);
  p.set("state", "NOT SUPPORTED");
  assert.deepEqual(p.visible().sort(), sourceLedger.experiments.filter(e => e.state.some(s => s.state === "NOT SUPPORTED")).map(e => e.id).sort());
  assert(p.visible().includes("qnp"));
  assert(!p.visible().includes("rain-atlas"));
  p.close();
});

test("search reaches limitations and intersects with question and state filters", () => {
  const p = page();
  p.set("search", "typography normalized");
  assert.deepEqual(p.visible(), []); // That historical entry is archived.
  p.set("archived", true);
  assert.deepEqual(p.visible(), ["rain-lab"]);
  p.set("question", "worlds");
  assert.equal(p.visible().length, 0);
  assert.equal(p.get("empty").hidden, false);
  assert.equal(p.get("export").disabled, true);
  p.close();
});

test("catalog-only projects do not become evidence claims", () => {
  const p = page();
  p.set("state", "unrecorded");
  assert(p.visible().includes("catalog-sentinel"));
  assert(!p.visible().includes("triad"));
  assert.match(p.get("catalog-sentinel").textContent, /no evidence-ledger entry/i);
  p.close();
});

test("comparison is bounded to three and survives filtering and URL restoration", () => {
  const p = page();
  ["triad", "qnp", "project-ascent"].forEach(p.select);
  assert.equal(p.get("comparison-content").children.length, 3);
  assert.equal(p.doc.querySelector('input[aria-label="Compare James"]').disabled, true);
  p.set("search", "never-a-result");
  assert.equal(p.visible().length, 0);
  assert.equal(p.get("comparison-content").children.length, 3);
  const q = page(p.window.location.hash);
  assert.equal(q.get("comparison-content").children.length, 3);
  assert.equal(q.get("search").value, "never-a-result");
  q.close();
  p.get("clear-comparison").click();
  assert.equal(p.get("comparison").hidden, true);
  assert.equal(p.doc.querySelector('input[aria-label="Compare James"]').disabled, false);
  p.close();
});

test("invalid hash input is ignored and archived permalinks open the record", () => {
  const p = page("#rain-lab");
  assert(p.visible().includes("rain-lab"));
  assert.equal(p.get("rain-lab").querySelector("details").open, true);
  p.close();
  const q = page("#view?state=FAKE&compare=no-such-record,triad,triad,qnp,project-ascent");
  assert.equal(q.get("state").value, "");
  assert(q.get("comparison-content").children.length <= 3);
  q.close();
  const r = page("#%E0%A4%A");
  assert.equal(r.visible().length, currentCount);
  r.close();
});

test("export contains only visible complete records, definitions and input hashes", async () => {
  const p = page();
  p.set("state", "SUPPORTED");
  p.get("export").click();
  assert.equal(p.downloads.length, 1);
  const exported = await new Promise(resolve => {
    const reader = new p.window.FileReader();
    reader.onload = () => resolve(JSON.parse(reader.result));
    reader.readAsText(p.downloads[0]);
  });
  assert.equal(exported.records.length, sourceLedger.experiments.filter(e => e.state.some(s => s.state === "SUPPORTED")).length);
  assert.equal(exported.filters.state, "SUPPORTED");
  assert(exported.states["NOT SUPPORTED"]);
  assert.match(exported.inputs["experiments/ledger.json"], /^[a-f0-9]{64}$/);
  assert.deepEqual(exported.records.find(r => r.id === "qnp").ledger, sourceLedger.experiments.find(e => e.id === "qnp"));
  p.close();
});

test("theme toggles and printing restores disclosure state", () => {
  const p = page();
  p.get("theme-toggle").click();
  assert.equal(p.doc.documentElement.dataset.theme, "dark");
  assert.equal(p.get("theme-toggle").textContent, "Light mode");
  p.get("theme-toggle").click();
  assert.equal(p.doc.documentElement.dataset.theme, "light");
  const details = p.get("triad").querySelector("details");
  assert.equal(details.open, false);
  p.window.dispatchEvent(new p.window.Event("beforeprint"));
  assert.equal(details.open, true);
  p.window.dispatchEvent(new p.window.Event("afterprint"));
  assert.equal(details.open, false);
  p.close();
});

test("without JavaScript every project and all evidence remain readable", () => {
  const dom = new JSDOM(html);
  assert.equal(dom.window.document.querySelectorAll(".record:not([hidden])").length, totalCount);
  assert.equal(dom.window.document.getElementById("filters").hidden, true);
  assert.match(dom.window.document.getElementById("triad").textContent, /NOT SUPPORTED/);
  dom.window.close();
});
