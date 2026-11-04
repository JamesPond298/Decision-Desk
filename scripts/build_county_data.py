#!/usr/bin/env python3
"""Build compact county election files from the Heideman v1.0.0 summary release."""
from __future__ import annotations
import csv
import io
import json
import pathlib
import urllib.request

SOURCE = "https://github.com/pmheideman/us-county-election-results/releases/download/v1.0.0/us_county_results_summary.csv"
OUT = pathlib.Path("data/county")
OFFICES = {"house", "senate"}
YEARS = set(range(2000, 2025, 2))

def number(value: str) -> int:
    try:
        return int(round(float(value)))
    except (TypeError, ValueError):
        return 0

def main() -> None:
    request = urllib.request.Request(SOURCE, headers={"User-Agent": "Decision-Desk county data builder"})
    with urllib.request.urlopen(request, timeout=120) as response:
        raw = response.read()
    if len(raw) < 1_000_000:
        raise SystemExit("County source download was unexpectedly small")

    groups: dict[tuple[str, int], list[dict[str, object]]] = {}
    reader = csv.DictReader(io.StringIO(raw.decode("utf-8-sig")))
    required = {"year", "office", "county_fips", "dem_votes", "rep_votes", "other_votes", "total_votes"}
    if not required.issubset(reader.fieldnames or []):
        raise SystemExit(f"Missing required columns: {sorted(required - set(reader.fieldnames or []))}")

    for row in reader:
        office = (row.get("office") or "").lower()
        year = number(row.get("year", ""))
        fips = (row.get("county_fips") or "").zfill(5)
        if office not in OFFICES or year not in YEARS or len(fips) != 5:
            continue
        item = {
            "fips": fips,
            "dem": number(row.get("dem_votes", "")),
            "rep": number(row.get("rep_votes", "")),
            "other": number(row.get("other_votes", "")),
            "total": number(row.get("total_votes", "")),
            "districts": number(row.get("n_districts", "")),
            "status": row.get("status") or "",
            "quality": row.get("quality_flag") or "",
        }
        groups.setdefault((office, year), []).append(item)

    OUT.mkdir(parents=True, exist_ok=True)
    for (office, year), rows in groups.items():
        rows.sort(key=lambda x: x["fips"])
        path = OUT / f"{office}-{year}.json"
        path.write_text(json.dumps({"office": office, "year": year, "rows": rows}, separators=(",", ":")), encoding="utf-8")

    manifest = {
        "dataset": "U.S. county-level election results v1.0.0",
        "source": "https://doi.org/10.5281/zenodo.22976553",
        "release": "https://github.com/pmheideman/us-county-election-results/releases/tag/v1.0.0",
        "license": "CC BY 4.0; upstream source terms remain applicable",
        "coverage": "Regular general elections; 48 contiguous states; documented gaps; no Alaska, Hawaii, or DC",
        "files": sorted(p.name for p in OUT.glob("*.json") if p.name != "manifest.json"),
    }
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    if len(manifest["files"]) < 20:
        raise SystemExit(f"Only built {len(manifest['files'])} county files")

if __name__ == "__main__":
    main()
