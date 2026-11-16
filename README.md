## (Claude Certified Architect — Foundations CCA certification)
 - [https://claudecertprep.com/cheatsheet]
 - https://www.clearcatnet.com/


| Format | Maximum | Why this limit |
| :--- | :--- | :--- |
| CSV (`.csv`) | 1 GB | Plain text, streams well. Loaded in chunks downstream. |
| JSON (`.json`) | 512 MB | A single JSON document is usually parsed whole, so memory is the limit. Use JSON Lines for bigger data. |
| EXCEL (`.xlsx`) | 100 MB | Zipped XML that expands about 10x when read; Excel itself stops at 1,048,576 rows. Use CSV or Parquet for large data. |
| ODS (`.ods`) | 100 MB | Same zipped-XML cost as `.xlsx`. |
| SHP (`.zip`) | 1 GB | Must contain `.shp`, `.shx` and `.dbf`. Each part is capped at 4 GB by the Shapefile spec. |
| GEOJSON (`.geojson`) | 512 MB | Single JSON document, parsed whole. |
| GEOJSON (`.json`) | 512 MB | Same as `.geojson`. |
| GEOPACKAGE (`.gpkg`) | 2 GB | SQLite database; can be large but is read by range, so it is safe at the single-request ceiling. |
| GML (`.gml`) | 512 MB | Verbose XML (often 10x the size of the same data in GeoPackage). |
| PDF (`.pdf`) | 100 MB | Documents, not datasets. Text extraction slows down sharply beyond this. |
| GEOTIFF (`.tif`) | 2 GB | Rasters are big; cloud-optimised GeoTIFF can be read by range. |
| GEOTIFF (`.tiff`) | 2 GB | Same as `.tif`. |
| LiDAR (`.las`) | 2 GB | Uncompressed point cloud; grows fast, so larger surveys need chunked upload. |
| LiDAR (`.laz`) | 2 GB | Compressed LAS (about 5-10x smaller), so 2 GB holds far more points. |
| NetCDF (`.nc`) | 2 GB | Scientific arrays; large files should be chunked or subset first. |
| GPX (`.gpx`) | 50 MB | GPS tracks are small XML; anything bigger is almost certainly the wrong file. |
| PARQUET (`.parquet`) | 2 GB | Columnar and compressed, so 2 GB is a lot of rows. Footer is checked for truncation. |


```

50 MB (smallest)	GPX
100 MB	Excel (.xlsx), ODS, PDF
512 MB	JSON, GeoJSON, GML
1 GB	CSV, SHP (.zip)
2 GB (largest)	GeoPackage, GeoTIFF, LiDAR, NetCDF, Parquet

````
