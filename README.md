## (Claude Certified Architect — Foundations CCA certification)
 - [https://claudecertprep.com/cheatsheet]
 - https://www.clearcatnet.com/

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

    <h2>Upload a Parquet file</h2>
    <input type="file" id="upload" accept=".parquet">
    <section id="uploaded"></section>

    <section id="tables"></section>
  </main>

  <script type="module">
    import { parquetReadObjects } from "https://esm.sh/hyparquet@1.31.5";

    const container = document.getElementById("tables");
    const esc = (v) => String(v).replace(/[&<>"']/g, ch => `&#${ch.charCodeAt(0)};`);

    async function showParquet(name, getBuffer, target = container) {
      const section = document.createElement("div");
      section.innerHTML = `<h2></h2><p>Loading...</p><table></table>`;
      section.querySelector("h2").textContent = name;
      target.appendChild(section);
      const status = section.querySelector("p");
      const table = section.querySelector("table");

      try {
        const rows = await parquetReadObjects({ file: await getBuffer() });
        console.log(`Loaded ${name} rows:`, rows);
        if (rows.length === 0) {
          status.textContent = "0 rows";
          return;
        }

        const cols = Object.keys(rows[0]);
        table.innerHTML =
          "<thead><tr>" + cols.map(c => `<th>${esc(c)}</th>`).join("") + "</tr></thead>" +
          "<tbody>" +
          rows.map(r => "<tr>" + cols.map(c => `<td>${esc(r[c])}</td>`).join("") + "</tr>").join("") +
          "</tbody>";
        status.textContent = `${rows.length} rows, ${cols.length} columns`;
      } catch (err) {
        status.textContent = "Failed to load: " + err.message;
      }
    }

    document.getElementById("upload").addEventListener("change", async (e) => {
      const file = e.target.files[0];
      const uploaded = document.getElementById("uploaded");
      uploaded.innerHTML = "";
      if (file) await showParquet(file.name, () => file.arrayBuffer(), uploaded);
    });

    for (const file of ["users.parquet", "orders.parquet"]) {
      await showParquet(file, async () => {
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

