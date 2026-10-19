## (Claude Certified Architect — Foundations CCA certification)
 - [https://claudecertprep.com/cheatsheet]
 - https://www.clearcatnet.com/

  <script type="module">
    import { parquetReadObjects } from "https://esm.sh/hyparquet@1.31.5";

    const status = document.getElementById("status");
    const table = document.getElementById("data");

    try {
      const res = await fetch("sample.parquet");
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const rows = await parquetReadObjects({ file: await res.arrayBuffer() });

      const cols = Object.keys(rows[0]);
      table.innerHTML =
        "<thead><tr>" + cols.map(c => `<th>${c}</th>`).join("") + "</tr></thead>" +
        "<tbody>" +
        rows.map(r => "<tr>" + cols.map(c => `<td>${String(r[c])}</td>`).join("") + "</tr>").join("") +
        "</tbody>";
      status.textContent = `${rows.length} rows, ${cols.length} columns`;
    } catch (err) {
      status.textContent = "Failed to load: " + err.message + " (serve this folder over http, not file://)";
    }
  </script>
