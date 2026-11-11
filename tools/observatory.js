/* Progressive enhancement for a completely self-contained reading edition. */
(() => {
  "use strict";
  const data = JSON.parse(document.getElementById("observatory-data").textContent);
  const byId = new Map(data.records.map(record => [record.id, record]));
  const nodes = new Map([...document.querySelectorAll("[data-record]")].map(node => [node.dataset.record, node]));
  const get = id => document.getElementById(id);
  const form = get("filters");
  const fields = ["search", "question", "state", "theme"];
  const selected = new Set();
  const searchText = new Map(data.records.map(r => [r.id, JSON.stringify(r).toLocaleLowerCase()]));
  let visible = [];
  let printDetails = [];
  let restoring = false;

  function notify(text) { get("announcement").textContent = text; }
  function state() {
    return Object.fromEntries([...fields.map(id => [id, get(id).value]), ["archived", get("archived").checked]]);
  }
  function updateLocation() {
    if (restoring) return;
    const values = state();
    const params = new URLSearchParams();
    fields.forEach(id => { if (values[id]) params.set(id, values[id]); });
    if (values.archived) params.set("archived", "1");
    if (selected.size) params.set("compare", [...selected].join(","));
    const hash = params.size ? "#view?" + params : "#catalog";
    try { history.replaceState(null, "", hash); } catch { /* Some file: viewers disable history. */ }
  }
  function filter() {
    const s = state();
    const terms = s.search.trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);
    visible = data.records.filter(r => {
      const e = r.ledger;
      return (s.archived || !["archived", "fork"].includes(r.status))
        && (!s.theme || r.theme === s.theme)
        && (!s.question || (s.question === "unrecorded" ? !e : e?.question === data.questions[s.question]))
        && (!s.state || (s.state === "unrecorded" ? !e : e?.state.some(item => item.state === s.state)))
        && terms.every(term => searchText.get(r.id).includes(term));
    });
    const ids = new Set(visible.map(r => r.id));
    nodes.forEach((node, id) => { node.hidden = !ids.has(id); });
    get("result-count").textContent = `${visible.length} of ${data.records.length} projects shown · ${visible.filter(r => r.ledger).length} with evidence records`;
    get("empty").hidden = visible.length !== 0;
    get("export").disabled = visible.length === 0;
    updateLocation();
  }
  function text(tag, value, parent) {
    const node = document.createElement(tag);
    node.textContent = value;
    parent.append(node);
    return node;
  }
  function paragraph(title, value, parent) { text("h4", title, parent); text("p", value, parent); }
  function compare() {
    const container = get("comparison-content");
    container.replaceChildren();
    container.style.setProperty("--columns", String(selected.size || 1));
    for (const id of selected) {
      const r = byId.get(id);
      const e = r.ledger;
      const card = document.createElement("article");
      text("h3", r.name, card);
      paragraph("Question", e?.question || "No evidence-ledger question recorded.", card);
      paragraph("Reviewed", e?.last_reviewed || (e ? data.ledger_reviewed : r.catalog_reviewed), card);
      text("h4", "Evidence & scope", card);
      if (e) {
        const list = document.createElement("ul");
        e.state.forEach(s => text("li", `${s.state} — ${s.scope}`, list));
        card.append(list);
      } else text("p", "No ledger entry. Catalog maturity is not an evidence verdict.", card);
      paragraph("Still open", e?.open || "No separate limitation recorded; read each state’s scope.", card);
      paragraph("Next experiment", e?.next || "No next experiment recorded.", card);
      text("h4", "Source records", card);
      const links = document.createElement("ul");
      const sources = e?.evidence?.length ? e.evidence : [r.links[0].url];
      sources.forEach((url, i) => {
        const li = document.createElement("li");
        const anchor = text("a", `Source ${i + 1} · ${new URL(url).pathname.split("/").pop() || "Project"}`, li);
        anchor.href = url;
        links.append(li);
      });
      card.append(links);
      container.append(card);
    }
    document.querySelectorAll(".compare-control input").forEach(input => {
      input.checked = selected.has(input.value);
      input.disabled = selected.size >= 3 && !input.checked;
    });
    get("comparison").hidden = selected.size === 0;
    get("compare-tray").hidden = selected.size === 0;
    get("selection-count").textContent = `${selected.size} of 3 selected`;
    updateLocation();
  }
  function restore() {
    restoring = true;
    form.reset();
    selected.clear();
    const hash = location.hash;
    if (hash.startsWith("#view?")) {
      const params = new URLSearchParams(hash.slice(6));
      fields.forEach(id => { get(id).value = params.get(id) || ""; });
      get("archived").checked = params.get("archived") === "1";
      (params.get("compare") || "").split(",").filter(id => byId.has(id)).slice(0, 3).forEach(id => selected.add(id));
    } else {
      let id;
      try { id = decodeURIComponent(hash.slice(1)); } catch { id = ""; }
      if (byId.has(id)) {
        get("archived").checked = ["archived", "fork"].includes(byId.get(id).status);
        nodes.get(id).querySelector("details").open = true;
      }
    }
    filter(); compare(); restoring = false;
    if (!hash.startsWith("#view?")) {
      let target;
      try { target = get(decodeURIComponent(hash.slice(1))); } catch { target = null; }
      target?.scrollIntoView();
    }
  }
  form.hidden = false;
  ["export", "filter-note", "theme-toggle"].forEach(id => { get(id).hidden = false; });
  document.querySelectorAll(".compare-control").forEach(node => { node.hidden = false; });
  form.addEventListener("submit", event => event.preventDefault());
  form.addEventListener("input", filter);
  form.addEventListener("reset", () => { if (!restoring) setTimeout(filter, 0); });
  document.querySelectorAll("[data-preset]").forEach(button => button.addEventListener("click", () => {
    form.reset();
    const preset = button.dataset.preset;
    if (preset === "failures") get("state").value = "NOT SUPPORTED";
    if (preset === "worlds") get("question").value = "worlds";
    if (preset === "gaps") get("state").value = "unrecorded";
    filter();
  }));
  document.querySelectorAll(".compare-control input").forEach(input => input.addEventListener("change", () => {
    if (input.checked && selected.size < 3) selected.add(input.value);
    else selected.delete(input.value);
    compare();
    notify(`${selected.size} projects selected. Choose View comparison to read them together.`);
  }));
  get("clear-comparison").addEventListener("click", () => {
    selected.clear(); compare(); get("catalog").focus(); notify("Comparison cleared.");
  });
  get("show-comparison").addEventListener("click", event => {
    event.preventDefault(); get("comparison").scrollIntoView(); get("comparison").focus({preventScroll: true});
  });
  get("export").addEventListener("click", () => {
    const payload = { ...data, records: visible, filters: state(), selected_ids: [...selected] };
    const url = URL.createObjectURL(new Blob([JSON.stringify(payload, null, 2) + "\n"], {type: "application/json"}));
    const anchor = document.createElement("a");
    anchor.href = url; anchor.download = "vers3dynamics-research-records.json";
    document.body.append(anchor); anchor.click(); anchor.remove();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
    notify(`Exported ${visible.length} visible records with source hashes and evidence definitions.`);
  });
  get("print").addEventListener("click", () => { document.body.dataset.print = "comparison"; window.print(); });
  window.addEventListener("beforeprint", () => {
    printDetails = [...document.querySelectorAll(".record:not([hidden]) details")].map(node => [node, node.open]);
    printDetails.forEach(([node]) => { node.open = true; });
  });
  window.addEventListener("afterprint", () => {
    delete document.body.dataset.print;
    printDetails.forEach(([node, open]) => { node.open = open; });
  });
  function dark() { return document.documentElement.dataset.theme === "dark" || (!document.documentElement.dataset.theme && matchMedia("(prefers-color-scheme: dark)").matches); }
  function themeLabel() { get("theme-toggle").textContent = dark() ? "Light mode" : "Dark mode"; }
  get("theme-toggle").addEventListener("click", () => {
    document.documentElement.dataset.theme = dark() ? "light" : "dark"; themeLabel();
  });
  matchMedia("(prefers-color-scheme: dark)").addEventListener("change", themeLabel);
  window.addEventListener("hashchange", () => {
    // Navigating to the comparison must not clear the very selection being viewed.
    if (location.hash === "#comparison") return;
    restore();
  });
  themeLabel(); restore();
})();
