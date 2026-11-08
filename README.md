## (Claude Certified Architect — Foundations CCA certification)
 - [https://claudecertprep.com/cheatsheet]
 - https://www.clearcatnet.com/

```
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Parquet Upload Test</title>
  <style>
    body { font-family: system-ui, sans-serif; padding: 2rem 1rem; max-width: 960px; margin: 0 auto; }
    .card { border: 1px solid #ddd; border-radius: 8px; padding: 2rem; text-align: center; }
    button { padding: .6rem 1.2rem; font-size: 1rem; border: 0; border-radius: 6px; background: #2563eb; color: #fff; cursor: pointer; }
    button:hover { background: #1d4ed8; }
    #status { margin-top: 1rem; color: #555; word-break: break-all; }
    #status.error { color: #b91c1c; }
    .table-wrap { margin-top: 1.5rem; overflow: auto; max-height: 60vh; border: 1px solid #ddd; border-radius: 8px; }
    table { border-collapse: collapse; width: 100%; font-size: .9rem; }
    th, td { padding: .4rem .7rem; border-bottom: 1px solid #eee; text-align: left; white-space: nowrap; }
    th { position: sticky; top: 0; background: #f5f5f5; }
  </style>
</head>
<body>
  <div class="card">
    <h1>Upload a Parquet file</h1>
    <input type="file" id="file-input" accept=".parquet,application/octet-stream" hidden>
    <button type="button" id="upload-btn">Upload</button>
    <p id="status">No file selected</p>
  </div>
  <div class="table-wrap" id="table-wrap" hidden></div>

  <p id="specMsg"></p>
  <table><thead><tr><th>in_column</th><th>out_column</th><th>type</th><th>nullable</th><th>description</th></tr></thead>
  <tbody id="colBody"></tbody></table>

  <script>
    // Classic script (no type="module"): the library is loaded with dynamic import() and cached in one promise.
    let _parquetPromise = null;

    function loadHyparquet() {
      if (_parquetPromise) return _parquetPromise;

      _parquetPromise = Promise.all([
        import("https://cdn.jsdelivr.net/npm/hyparquet@1.31.0/+esm"),
        // hyparquet reads only UNCOMPRESSED/SNAPPY by default; this adds GZIP, ZSTD, BROTLI, LZ4.
        import("https://cdn.jsdelivr.net/npm/hyparquet-compressors@1.1.2/+esm"),
      ])
        .then(([hp, comp]) => {
          if (!hp.parquetReadObjects || !hp.parquetMetadata) {
            throw new Error("hyparquet exports not found");
          }
          return {
            parquetReadObjects: hp.parquetReadObjects,
            parquetMetadata: hp.parquetMetadata,
            compressors: comp.compressors,
          };
        })
        .catch((err) => { _parquetPromise = null; throw err; });   // allow a retry after a failed load

      return _parquetPromise;
    }

    const input = document.getElementById('file-input');
    const btn = document.getElementById('upload-btn');
    const status = document.getElementById('status');
    const wrap = document.getElementById('table-wrap');
    const MAX_ROWS = 1000;
    let records;

    btn.addEventListener('click', () => input.click());

    const $ = (sel) => document.querySelector(sel);
    const slug = (s) => String(s).toLowerCase().replace(/[^a-z0-9]+/g, '_').replace(/^_+|_+$/g, '');

    // [{a:1,b:2}, {a:3,b:4}] -> [["a","b"], ["1","2"], ["3","4"]]: header row first, then one array per record.
    function toArrays(rows) {
      if (rows.length === 0) return [];
      const cols = Object.keys(rows[0]);
      return [
        cols,
        ...rows.map(r =>
          cols.map(c => {
            const value = r[c];
            return value == null || String(value).trim().toLowerCase() === 'null'
              ? ''
              : String(value);
          })
        )
      ];
    }

    // Parquet field -> string | int | bigint | double | decimal | date | timestamp | boolean
    // Never returns BYTE_ARRAY / INT96 / FIXED_LEN_BYTE_ARRAY.
    function parquetTypeToSimple(f) {
      const lt = f.logical_type || {}, ct = f.converted_type, T = f.type;
      if (f.num_children) return 'string';                               // nested struct/list/map
      if (lt.type === 'DECIMAL' || ct === 'DECIMAL') return 'decimal';
      if (lt.type === 'DATE' || ct === 'DATE') return 'date';
      if (lt.type === 'TIMESTAMP' || ct === 'TIMESTAMP_MILLIS' || ct === 'TIMESTAMP_MICROS' || T === 'INT96') return 'timestamp';
      if (lt.type === 'TIME' || ct === 'TIME_MILLIS' || ct === 'TIME_MICROS') return 'string';
      if (lt.type === 'INTEGER' || /^U?INT_/.test(ct || '')) {
        const bits = lt.bitWidth ?? Number((ct || '').replace(/\D/g, ''));
        const unsigned = lt.isSigned === false || /^UINT/.test(ct || '');
        if (unsigned && bits === 64) return 'decimal';                   // doesn't fit in a signed bigint
        return bits === 64 || (unsigned && bits === 32) ? 'bigint' : 'int';
      }
      switch (T) {
        case 'BOOLEAN': return 'boolean';
        case 'INT32':   return 'int';
        case 'INT64':   return 'bigint';
        case 'FLOAT':
        case 'DOUBLE':  return 'double';
        default:        return 'string';                                 // BYTE_ARRAY etc.
      }
    }

    // schema is a flat list; keep top-level columns only (a nested parent counts as one column)
    function topLevelColumns(schema) {
      const cols = [];
      const size = (i) => { let n = 1; for (let k = 0; k < (schema[i].num_children || 0); k++) n += size(i + n); return n; };
      for (let i = 1; i < schema.length; i += size(i)) cols.push(schema[i]);   // schema[0] = root row, skipped
      return cols;
    }

    // Builds { in_column, out_column, type, nullable, description } per column from the Parquet schema.
    function applyParquetSchema(schema, sourceLabel) {
      const msg = $('#specMsg');
      const seen = new Set(), cols = [];
      topLevelColumns(schema).forEach(f => {
        const s = slug(f.name); if (!s || seen.has(s)) return; seen.add(s);
        const lt = f.logical_type || {};
        const type = parquetTypeToSimple(f);
        cols.push({
          in_column: f.name,
          out_column: s,
          type,
          description: type === 'decimal' ? `DECIMAL(${lt.precision ?? f.precision ?? 20},${lt.scale ?? f.scale ?? 0})` : '',
          nullable: f.repetition_type !== 'REQUIRED'
        });
      });

      console.log(`applyParquetSchema: ${cols.length} columns`, cols);
      if (!cols.length) { msg.textContent = 'No columns found in the file.'; return []; }

      renderColumnsTable(cols);
      msg.textContent = `✓ ${cols.length} columns from ${sourceLabel} (types read from the Parquet schema).`;
      return cols;
    }

    function renderColumnsTable(cols) {
      const body = $('#colBody'); body.replaceChildren();
      cols.forEach(c => {
        const tr = body.insertRow();
        [c.in_column, c.out_column, c.type, c.nullable ? 'yes' : 'no', c.description]
          .forEach(t => { tr.insertCell().textContent = t; });
      });
    }

    input.addEventListener('change', async () => {
      const f = input.files[0];
      if (!f) return;
      status.className = '';
      status.textContent = `Reading ${f.name} (${(f.size / 1024).toFixed(1)} KB)…`;
      wrap.hidden = true;

      try {
        const { parquetReadObjects, parquetMetadata, compressors } = await loadHyparquet();
        const file = await f.arrayBuffer();
        const metadata = parquetMetadata(file);
        console.log(`parquetMetadata: ${metadata.num_rows} rows`, metadata.schema);
        // Schema first: it shows even if reading the row data fails below.
        applyParquetSchema(metadata.schema, f.name);

        // hyparquet cannot decode INTERVAL / BSON values: skip those columns when reading rows.
        const topCols = topLevelColumns(metadata.schema);
        const skipped = topCols.filter(c => c.converted_type === 'INTERVAL' || c.converted_type === 'BSON').map(c => c.name);
        const columns = skipped.length ? topCols.map(c => c.name).filter(n => !skipped.includes(n)) : undefined;
        const rows = await parquetReadObjects({ file, compressors, columns });
        console.log(`parquetReadObjects rows: ${rows.length} rows`, rows);

        // records = toArrays(rows);
        // console.log(`records: ${records.length}`, records);

        status.textContent = `${f.name}: ${rows.length} rows` +
          (rows.length > MAX_ROWS ? ` (showing first ${MAX_ROWS})` : '') +
          (skipped.length ? ` · not shown (unsupported type): ${skipped.join(', ')}` : '');
        render(rows.slice(0, MAX_ROWS));
      } catch (err) {
        console.error(err);
        status.className = 'error';
        status.textContent = `Failed to read parquet: ${err.message}`;
      }
    });

    function fmt(v) {
      if (v === null || v === undefined) return '';
      if (typeof v === 'bigint') return v.toString();
      if (v instanceof Date) return isNaN(v) ? String(v) : v.toISOString();   // out-of-range dates would throw
      if (v instanceof Uint8Array) {                                           // binary / UUID / checksum
        const hex = [...v.slice(0, 16)].map(b => b.toString(16).padStart(2, '0')).join('');
        return '0x' + hex + (v.length > 16 ? `… (${v.length} bytes)` : '');
      }
      if (typeof v === 'object') {
        return JSON.stringify(v, (_, x) => (typeof x === 'bigint' ? x.toString() : x));
      }
      return String(v);
    }

    function render(rows) {
      wrap.replaceChildren();
      if (!rows.length) return;
      const cols = Object.keys(rows[0]);
      const table = document.createElement('table');
      const head = table.createTHead().insertRow();
      cols.forEach(c => { const th = document.createElement('th'); th.textContent = c; head.appendChild(th); });
      const body = table.createTBody();
      for (const row of rows) {
        const tr = body.insertRow();
        cols.forEach(c => { tr.insertCell().textContent = fmt(row[c]); });
      }
      wrap.appendChild(table);
      wrap.hidden = false;
    }
  </script>
</body>
</html>



```

```
// [{a:1,b:2}, {a:3,b:4}] -> [["a","b"], [1,2], [3,4]]: header row first, then one array per record.
 console.log('temp', JSON.stringify(toArrays(records))); // JSON.stringify prints strings with double quotes
    function toArrays(rows) {
      if (rows.length === 0) return [];
      const cols = Object.keys(rows[0]);
      return [cols, ...rows.map(r => cols.map(c => String(r[c])))];
    }

```
   
```
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Home</title>
  <style>
    body {
      font-family: system-ui, sans-serif;
      margin: 0;
      color: #222;
      background: #f7f7f9;
    }
    header, footer {
      padding: 1rem 2rem;
      background: #1f2937;
      color: #fff;
    }
    nav a {
      color: #fff;
      margin-right: 1rem;
      text-decoration: none;
    }
    main {
      max-width: 800px;
      margin: 2rem auto;
      padding: 0 1rem;
    }
    table { border-collapse: collapse; width: 100%; background: #fff; }
    th, td { border: 1px solid #ddd; padding: 0.5rem 0.75rem; text-align: left; }
    th { background: #e5e7eb; }
  </style>
</head>
<body>
  <header>
    <h1>Parquet File Project</h1>
    <nav>
      <a href="home.html">Home</a>
    </nav>
  </header>

  <main>
    <h2>Welcome</h2>
    <p>This project creates and works with Parquet files using Python and PyArrow.</p>
    <ul>
      <li><code>create_parquet.py</code> generates the sample data.</li>
      <li><code>users.parquet</code> and <code>orders.parquet</code> hold the output tables.</li>
    </ul>

    <h2>Upload a file</h2>
    <p>Supports Parquet, CSV and Excel (.xlsx, .xls). The file is read in your browser and is not sent anywhere.</p>
    <input type="file" id="upload" accept=".parquet,.csv,.xlsx,.xls">
    <section id="uploaded"></section>

    <section id="tables"></section>
  </main>

  <script type="module">
    import { parquetReadObjects } from "https://esm.sh/hyparquet@1.31.5";
    import * as XLSX from "https://esm.sh/xlsx@0.18.5";

    const MAX_ROWS_SHOWN = 1000; // rendering every row of a big file would freeze the page
    const container = document.getElementById("tables");
    const esc = (v) => String(v).replace(/[&<>"']/g, ch => `&#${ch.charCodeAt(0)};`);

    // Each reader returns [{ title, rows }]: one entry per table (Excel can have several sheets).
    async function readTables(name, buffer) {
      const ext = name.split(".").pop().toLowerCase();
      if (ext === "parquet") {
        return [{ title: name, rows: await parquetReadObjects({ file: buffer }) }];
      }
      if (ext === "csv" || ext === "xlsx" || ext === "xls") {
        const wb = XLSX.read(buffer, { type: "array" });
        return wb.SheetNames.map(sheet => ({
          title: ext === "csv" ? name : `${name} - ${sheet}`,
          rows: XLSX.utils.sheet_to_json(wb.Sheets[sheet], { defval: "" }),
        }));
      }
      throw new Error(`Unsupported file type: .${ext}`);
    }

    function renderTable(target, title, rows) {
      const section = document.createElement("div");
      section.innerHTML = `<h2></h2><p></p><table></table>`;
      section.querySelector("h2").textContent = title;
      target.appendChild(section);
      const status = section.querySelector("p");
      if (rows.length === 0) {
        status.textContent = "0 rows";
        return;
      }

      const cols = Object.keys(rows[0]);
      const shown = rows.slice(0, MAX_ROWS_SHOWN);
      section.querySelector("table").innerHTML =
        "<thead><tr>" + cols.map(c => `<th>${esc(c)}</th>`).join("") + "</tr></thead>" +
        "<tbody>" +
        shown.map(r => "<tr>" + cols.map(c => `<td>${esc(r[c])}</td>`).join("") + "</tr>").join("") +
        "</tbody>";
      status.textContent = `${rows.length} rows, ${cols.length} columns` +
        (rows.length > shown.length ? ` (showing first ${shown.length})` : "");
    }

    async function showFile(name, getBuffer, target = container) {
      try {
        for (const { title, rows } of await readTables(name, await getBuffer())) {
          console.log(`Loaded ${title} rows:`, rows);
          renderTable(target, title, rows);
        }
      } catch (err) {
        const p = document.createElement("p");
        p.textContent = `Failed to load ${name}: ${err.message}`;
        target.appendChild(p);
      }
    }

    document.getElementById("upload").addEventListener("change", async (e) => {
      const file = e.target.files[0];
      const uploaded = document.getElementById("uploaded");
      uploaded.innerHTML = "";
      if (file) await showFile(file.name, () => file.arrayBuffer(), uploaded);
    });

    for (const file of ["users.parquet", "orders.parquet"]) {
      await showFile(file, async () => {
        const res = await fetch(file);
        if (!res.ok) throw new Error(`HTTP ${res.status} (serve this folder over http, not file://)`);
        return res.arrayBuffer();
      });
    }
  </script>

  <footer>
    <p>&copy; 2026</p>
  </footer>
</body>
</html>
```




````
