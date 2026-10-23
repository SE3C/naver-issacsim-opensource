/**
 * NCRC public-data exporter
 * Scope: public/read-only data only.
 * - GET only
 * - same-origin only
 * - does NOT call auth/team/study/submission/server/private endpoints
 * - discovered API strings are inventoried but NOT requested automatically
 *
 * Run in DevTools Console on https://robotics.connect.or.kr/
 */
(async () => {
  const ORIGIN = location.origin;
  const NOW = new Date();
  const stamp = NOW.toISOString().replace(/[:.]/g, "-");

  const PUBLIC_ENDPOINTS = [
    "/researchlog/videos.json",
    `/researchlog/stats.json?t=${Date.now()}`,
    "/api/competition/current",
    "/api/evaluation-rank?competitionId=1",
    "/api/video",
    "/api/tournament?competitionId=1",
    "/api/tournament/finalRank?competitionId=1",
    "/api/notice",
    "/api/addlink"
  ];

  const PUBLIC_PAGES = ["/", "/status", "/researchlog/"];

  const SENSITIVE_PATH_RE =
    /\/api\/(?:auth|user|team|study-file|preliminary-file|file\/upload|server)(?:\/|\?|$)/i;

  function safeUrl(path) {
    const u = new URL(path, ORIGIN);
    if (u.origin !== ORIGIN) throw new Error(`cross-origin blocked: ${u.href}`);
    return u;
  }

  async function fetchRecord(path, { text = false } = {}) {
    const u = safeUrl(path);
    const started = performance.now();
    try {
      const r = await fetch(u.href, {
        method: "GET",
        cache: "no-store",
        credentials: "same-origin"
      });

      const bodyText = await r.text();
      const ct = r.headers.get("content-type") || "";
      let data = null;
      let parseError = null;

      if (!text && /json/i.test(ct)) {
        try { data = JSON.parse(bodyText); }
        catch (e) { parseError = String(e); }
      } else if (!text) {
        try { data = JSON.parse(bodyText); }
        catch { data = null; }
      }

      return {
        url: u.href,
        path: u.pathname + u.search,
        status: r.status,
        ok: r.ok,
        contentType: ct,
        elapsedMs: Math.round((performance.now() - started) * 10) / 10,
        fetchedAt: new Date().toISOString(),
        parseError,
        data,
        text: text ? bodyText : (data === null ? bodyText : undefined)
      };
    } catch (e) {
      return {
        url: u.href,
        path: u.pathname + u.search,
        status: null,
        ok: false,
        contentType: null,
        elapsedMs: Math.round((performance.now() - started) * 10) / 10,
        fetchedAt: new Date().toISOString(),
        error: String(e)
      };
    }
  }

  // Normalize array indices so schemas merge cleanly: foo[0].bar -> foo[].bar
  function visit(value, base, rows, source) {
    const type =
      value === null ? "null" :
      Array.isArray(value) ? "array" :
      typeof value;

    rows.push({ source, path: base || "root", type, value });

    if (Array.isArray(value)) {
      for (const v of value) visit(v, `${base || "root"}[]`, rows, source);
    } else if (value && typeof value === "object") {
      for (const [k, v] of Object.entries(value)) {
        visit(v, base ? `${base}.${k}` : `root.${k}`, rows, source);
      }
    }
  }

  function scalarSample(v) {
    if (v === null) return null;
    if (typeof v === "string") return v.length > 180 ? v.slice(0, 177) + "..." : v;
    if (typeof v === "number" || typeof v === "boolean") return v;
    if (Array.isArray(v)) return `[array:${v.length}]`;
    if (typeof v === "object") return "{object}";
    return String(v);
  }

  function buildCatalog(records) {
    const flat = [];
    for (const [source, rec] of Object.entries(records)) {
      if (rec?.data !== null && rec?.data !== undefined) {
        visit(rec.data, "", flat, source);
      }
    }

    const m = new Map();
    for (const row of flat) {
      const key = `${row.source}\u0000${row.path}`;
      if (!m.has(key)) {
        m.set(key, {
          source: row.source,
          path: row.path,
          count: 0,
          nullCount: 0,
          types: new Set(),
          samples: [],
          distinctScalars: new Set()
        });
      }
      const x = m.get(key);
      x.count++;
      x.types.add(row.type);
      if (row.value === null) x.nullCount++;

      if (row.type !== "object" && row.type !== "array") {
        const s = scalarSample(row.value);
        const token = JSON.stringify(s);
        if (x.samples.length < 8 && !x.samples.some(v => JSON.stringify(v) === token)) {
          x.samples.push(s);
        }
        if (x.distinctScalars.size <= 100) x.distinctScalars.add(token);
      }
    }

    return [...m.values()]
      .map(x => ({
        source: x.source,
        path: x.path,
        count: x.count,
        nullCount: x.nullCount,
        types: [...x.types].sort().join("|"),
        distinctScalarCount:
          x.distinctScalars.size > 100 ? ">100" : x.distinctScalars.size,
        samples: x.samples
      }))
      .sort((a, b) =>
        a.source.localeCompare(b.source) || a.path.localeCompare(b.path)
      );
  }

  function extractStrings(src) {
    const apis = new Set();
    const routes = new Set();

    for (const m of src.matchAll(/["'`](\/api\/[^"'`\s\\]{1,220})["'`]/g)) {
      apis.add(m[1]);
    }

    for (const m of src.matchAll(/["'`](\/(?:researchlog|status|board|login|info|promise)(?:\/[^"'`\s\\]{0,180})?)["'`]/g)) {
      routes.add(m[1]);
    }

    return {
      apiLiterals: [...apis].sort(),
      routeLiterals: [...routes].sort()
    };
  }

  function csvEscape(v) {
    if (v === null || v === undefined) return "";
    const s = typeof v === "string" ? v : JSON.stringify(v);
    return /[",\n\r]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s;
  }

  function toCsv(rows) {
    const headers = [
      "source", "path", "count", "nullCount",
      "types", "distinctScalarCount", "samples"
    ];
    return [
      headers.join(","),
      ...rows.map(r => headers.map(h => csvEscape(r[h])).join(","))
    ].join("\n");
  }

  function download(name, text, mime) {
    const blob = new Blob([text], { type: mime });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = name;
    document.body.appendChild(a);
    a.click();
    a.remove();
    setTimeout(() => URL.revokeObjectURL(a.href), 5000);
  }

  console.log("[1/5] Fetching known public JSON endpoints...");

  const responses = {};
  for (const path of PUBLIC_ENDPOINTS) {
    if (SENSITIVE_PATH_RE.test(path)) {
      responses[path] = { skipped: true, reason: "sensitive/private scope" };
      continue;
    }
    responses[path] = await fetchRecord(path);
    console.log(path, responses[path].status);
  }

  console.log("[2/5] Fetching public page HTML...");
  const pages = {};
  for (const path of PUBLIC_PAGES) {
    const rec = await fetchRecord(path, { text: true });
    const strings = rec.text ? extractStrings(rec.text) : { apiLiterals: [], routeLiterals: [] };
    pages[path] = {
      ...rec,
      discoveredApiLiterals: strings.apiLiterals,
      discoveredRouteLiterals: strings.routeLiterals
    };
  }

  console.log("[3/5] Inspecting already-loaded same-origin JS bundles...");
  const jsUrls = [...new Set([
    ...[...document.scripts].map(s => s.src),
    ...performance.getEntriesByType("resource").map(x => x.name)
  ].filter(u =>
    u &&
    u.startsWith(ORIGIN) &&
    /\.js(?:\?|$)/i.test(u)
  ))];

  const bundles = [];
  const discoveredApis = new Set();
  const discoveredRoutes = new Set();

  for (const url of jsUrls) {
    try {
      const src = await fetch(url, { cache: "no-store", credentials: "same-origin" }).then(r => r.text());
      const ex = extractStrings(src);
      ex.apiLiterals.forEach(x => discoveredApis.add(x));
      ex.routeLiterals.forEach(x => discoveredRoutes.add(x));

      bundles.push({
        url,
        file: new URL(url).pathname.split("/").pop(),
        bytes: new Blob([src]).size,
        apiLiterals: ex.apiLiterals,
        routeLiterals: ex.routeLiterals
      });
    } catch (e) {
      bundles.push({ url, error: String(e) });
    }
  }

  console.log("[4/5] Building field catalog...");

  const catalogSources = {};
  for (const [path, rec] of Object.entries(responses)) {
    if (rec && rec.data !== undefined) catalogSources[path] = rec;
  }
  const fieldCatalog = buildCatalog(catalogSources);

  // Useful derived researchlog views without altering raw data
  const videosRec = responses["/researchlog/videos.json"]?.data;
  const statsKey = Object.keys(responses).find(k => k.startsWith("/researchlog/stats.json"));
  const statsRec = statsKey ? responses[statsKey]?.data : null;

  const derived = {
    researchlog: {
      statsRootKeys: statsRec && typeof statsRec === "object" && !Array.isArray(statsRec)
        ? Object.keys(statsRec).sort() : [],
      videosRootKeys: videosRec && typeof videosRec === "object" && !Array.isArray(videosRec)
        ? Object.keys(videosRec).sort() : [],
      fallsCurve: statsRec?.falls_curve ?? null,
      fallsN: statsRec?.falls_n ?? null,
      avgFall: statsRec?.avg_fall ?? null,
      values: statsRec?.values ?? null,
      rate: statsRec?.rate ?? null
    },
    endpointInventory: {
      requestedPublicEndpoints: PUBLIC_ENDPOINTS,
      discoveredApiLiterals: [...discoveredApis].sort(),
      discoveredRouteLiterals: [...discoveredRoutes].sort(),
      notAutoRequestedBecauseDiscoveryOnly:
        [...discoveredApis].filter(x => !PUBLIC_ENDPOINTS.some(p => p === x)).sort()
    }
  };

  const resourceInventory = performance.getEntriesByType("resource").map(x => ({
    name: x.name,
    initiatorType: x.initiatorType,
    duration: x.duration,
    transferSize: x.transferSize,
    encodedBodySize: x.encodedBodySize,
    decodedBodySize: x.decodedBodySize
  }));

  const out = {
    meta: {
      exporter: "NCRC public-data exporter",
      version: 1,
      origin: ORIGIN,
      exportedAt: new Date().toISOString(),
      pageAtExport: location.href,
      scope: "public/read-only only; no private/authenticated team data requested",
      requestMethod: "GET only"
    },
    responses,
    pages,
    bundles,
    resourceInventory,
    derived,
    fieldCatalog
  };

  console.log("[5/5] Downloading export files...");

  download(
    `ncrc_public_export_${stamp}.json`,
    JSON.stringify(out, null, 2),
    "application/json;charset=utf-8"
  );

  download(
    `ncrc_public_field_catalog_${stamp}.csv`,
    "\ufeff" + toCsv(fieldCatalog),
    "text/csv;charset=utf-8"
  );

  download(
    `ncrc_public_endpoint_inventory_${stamp}.json`,
    JSON.stringify(derived.endpointInventory, null, 2),
    "application/json;charset=utf-8"
  );

  console.log("DONE", {
    endpoints: Object.keys(responses).length,
    fieldPaths: fieldCatalog.length,
    bundles: bundles.length,
    discoveredApis: discoveredApis.size,
    discoveredRoutes: discoveredRoutes.size
  });

  console.log(
    "Downloaded:",
    `ncrc_public_export_${stamp}.json`,
    `ncrc_public_field_catalog_${stamp}.csv`,
    `ncrc_public_endpoint_inventory_${stamp}.json`
  );

  return out;
})();
