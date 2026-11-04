# Decision Desk — Election Intelligence

A broadcast-style, static-hosted county election research dashboard for GitHub Pages. Built with HTML, CSS, JavaScript, D3 and TopoJSON; no server or secret API keys.

## Working features
- National and state drill-down map of U.S. counties with click/hover inspection and zoom.
- Historical county presidential results for 2000–2024 from Election Data/MIT, plus county-level regular general-election U.S. Senate and House returns for 2000–2024 from the [Heideman v1.0.0 compilation](https://doi.org/10.5281/zenodo.22976553) (CC BY 4.0, documented gaps, 48 contiguous states).
- Election year / race selection; a 2026 comparison control for 2024, 2022 or 2020 baselines; historical county lean labels; and CSV imports for the user's own sources.
- County vote totals, D-R vote margins, cross-year county history, national aggregates and CSV export.
- Full-screen broadcast mode, responsive design, visible source availability, and clear missing-data states.
- 2026 and 2028 cycle placeholders (no invented returns).
- Temporary AP or Decision Desk HQ live-provider mode through a user-supplied secure relay URL. Live mode expires at 6:00 a.m. the following morning and falls back to the free historical provider.

## Not yet implemented
- Automated county Senate, House and Governor archives. The widely available MIT Senate and House datasets are *statewide* and *district-wide*, not county-level; do not treat those totals as county results. County-to-congressional-district splits require extra geography and returns data.
- Reliable official 2026 county results, live election-night reporting, polling-place reporting, registered-voter turnout, early ballots, expected-turnout projections or modeled remaining votes.
- Fully computed swing layer; it is intentionally rendered neutral until compatible comparisons are implemented.
- A backend to cache and validate licensed live feeds. GitHub Pages is static hosting only; never place paid API credentials in browser JavaScript.

## Deploy to GitHub Pages
1. Use the existing repository `JamesPond298/Decision-Desk` (public visibility is generally needed for GitHub Pages on GitHub Free).
2. The files `index.html`, `styles.css`, `app.js`, `.nojekyll` and `README.md` are already committed to the repository root.
3. Open repository **Settings → Pages → Build and deployment**; choose **Deploy from a branch**, branch **main**, folder **/(root)**, then Save.
4. The site will appear at `https://JamesPond298.github.io/Decision-Desk/` after GitHub Pages deploys it. This web app requires internet access to load its JS mapping libraries, map boundaries, and historical data.

## Live provider relay

GitHub Pages is public static hosting, so AP or Decision Desk HQ credentials must never be placed in `config.js` or browser JavaScript. Run a private server-side relay that stores the vendor key and expose only its HTTPS results endpoint.

The dashboard requests:

```
GET {relay}?provider=AP&year=2026&race=SENATE
GET {relay}?provider=DDHQ&year=2026&race=HOUSE
```

The relay should return JSON as `{ "rows": [...] }`. County rows may use the same fields as the CSV importer. State-level rows should include `state_fips` (or `state_po`), candidate, party, votes, year, stage and special. The browser never receives the vendor credential.

## County CSV import
Select a year and race in the dashboard and import CSV with one row per county/candidate or county/party. The parser accepts columns:

```
year,office,county_fips,party,candidatevotes,totalvotes
2022,SENATE,28001,DEMOCRAT,1500,3700
2022,SENATE,28001,REPUBLICAN,2100,3700
2022,SENATE,28001,OTHER,100,3700
```

The numbers above are *fabricated format examples* only. County FIPS should have 5 digits including leading zeros. Accepted race values are `PRESIDENT`, `SENATE`, `HOUSE`, `GOVERNOR`. Imported CSV is retained only in this browser tab until reload; it does not save to your GitHub repo. For split-county House districts, the current CSV importer sums votes across all races that share the county; a subsequent release must add district-aware filtering before using these totals for comparative analyses.

## Attribution
Presidential results originate with MIT Election Data and Science Lab, "County Presidential Election Returns 2000-2024", [Harvard Dataverse](https://doi.org/10.7910/DVN/VOQCHQ), under CC0. Geographic files use [us-atlas](https://github.com/topojson/us-atlas). County maps and data are subject to upstream network availability. This independent project is not affiliated with an election authority or broadcaster.

## Design principles
Never interpret missing as zero; never label total votes as turnout rate; distinguish certified returns from unofficial returns, estimates and local imports; never make a race call from a map color alone.