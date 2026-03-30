# Data Visualization Best Practices

An interactive guide to data visualization best practices, built by Josh Noble and Ben Kates, Data Designers. The site is deployed on GitHub Pages at https://joshuajnoble.github.io/method-data-viz/.

Each page covers a different topic — data fundamentals, chart types, distributions, etc. — with live, interactive Plotly charts that readers can explore directly in the browser.

## Local Development

> **TODO:** Confirm whether Devbox, plain pip/venv, or both are the supported setup path.

The project uses [uv](https://docs.astral.sh/uv/) as the Python package manager. `local_build.sh` installs `uv` from scratch, runs the build, and starts a local server.

To develop a single app interactively, run it with marimo directly:

```sh
uv run marimo edit apps/basic_principles.py --sandbox
```

## Why Marimo

[Marimo](https://marimo.io/) is a reactive Python notebook framework. Cells re-execute automatically when their dependencies change, which makes it great for building interactive data explorations without writing frontend code. It's particularly well-suited for work that will be shown to non-technical audiences. The end result looks and feels like a polished app, not a code notebook.

Critically, marimo can **export apps to HTML + WebAssembly**. The exported apps run entirely client-side in the browser via [Pyodide](https://pyodide.org/), which means they can be hosted on GitHub Pages with no backend server. This is how the site is deployed.

## Dataset

Some of the demo data is from the [Superstore Sales dataset](https://community.tableau.com/s/question/0D54T00000CWeX8SAL/sample-superstore-sales-excelxls) commonly used in data science and visualization tutorials. It contains ~10K rows of fictional retail orders with columns for sales, profit, category, segment, region, dates, etc.

## Data Generation Notebooks

`data_generation.ipynb` and `data_generation2.ipynb` are Jupyter notebooks that transform `superstore.csv` into the pre-aggregated CSVs that live in `apps/public/`. These notebooks are run manually and their outputs are included in the repo — they are not part of the automated build.

## App Structure

Each `.py` file in `apps/` is a marimo app that corresponds to one page of the site:

> **TODO:** update once more have been merged

| File | Page |
|------|------|
| `data_fundamentals.py` | Data Fundamentals |
| `basic_principles.py` | Basic Principles |
| `viz_types.py` | Chart Types |
| `segments_and_percentages.py` | Parts and Wholes |
| `distributions.py` | Distributions |
| `events_and_ts.py` | Events and Time Series |

### Inline Script Metadata

Each app file starts with a `# /// script` block that declares its Python dependencies. This is the [PEP 723](https://peps.python.org/pep-0723/) inline metadata format. When marimo exports with `--sandbox`, it reads this block to know which packages to bundle into the WASM build. **It's important to note that any depndency required by the page must be added here**.

### Loading Data in WASM

When an app runs locally, it can read files from disk normally. When it runs as WASM in the browser, there's no filesystem — files must be fetched over HTTP. The helpers `gh_pages_read_csv_into_df()` and `gh_pages_load_image()` in `apps/public/my_utils.py` handle this transparently: they check whether the app is running locally or over HTTP, and use either `pd.read_csv()` or Pyodide's `pyfetch` accordingly.

## Shared Utilities (`apps/public/my_utils.py`)

This file is imported by every app/page and provides functions for data loading (see above), Method color palette, `plotly` theme defaults/formatting, stylized callout boxes, and number formatting (ie: `1200` → `1.2K`).

## Custom CSS

`custom.css` themes marimo's UI to the Method brand including fonts, brand colors, and callout styles.

There are two copies of this file: one at the repo root (`custom.css`) and one in `apps/custom.css`. The root copy is used by the build script (copied into `_site/`) for the deployed site. The `apps/` copy is picked up by marimo when running apps locally during development. Both files should be kept in sync.

> **TODO:** `head.html` for custom JS (not merged from other branch).

## Build & Deploy

### How the Build Works

The build script (`.github/scripts/build.py`) does the following:

1. Copies static assets (`custom.css`, `apps/public/`) into `_site/`.
2. Exports each app in `apps/` to HTML+WASM using `marimo export html-wasm --sandbox`, producing `*_iframe.html` files.
3. Wraps each exported app in a shell page using the Jinja2 template `templates/app_shell.html.j2`. The shell adds a responsive sidebar navigation and embeds the WASM app in an iframe.
4. Generates an `index.html` that redirects to the first app.

### `templates/apps_nav.json`

This JSON file controls the order and display labels of pages in the sidebar. Each entry maps an app file path to a label:

```json
[
  { "path": "apps/data_fundamentals.py", "label": "Data Fundamentals" },
  { "path": "apps/basic_principles.py", "label": "Basic Principles" },
  ...
]
```

Apps not listed here are excluded from the navigation. To add a new page, add the `.py` file to `apps/` and add an entry here.

### `_site/` Output

`_site/` is the generated build output and is gitignored. Do not edit files in it directly — they are overwritten on every build.

### Production (GitHub Actions)

On push to `main`, the workflow in `.github/workflows/gh-pages-deploy.yml` runs the build script and deploys `_site/` to GitHub Pages automatically.

### Local Build

See the [Local Development](#local-development) section above for commands.