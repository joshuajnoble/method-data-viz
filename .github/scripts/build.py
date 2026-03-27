"""
Build script for marimo apps.

This script exports marimo apps to HTML/WebAssembly format, generates
shell pages with sidenav, and writes a root index.html redirect.

The script can be run from the command line with optional arguments:
    uv run .github/scripts/build.py [--output-dir OUTPUT_DIR]

The exported files will be placed in the specified output directory (default: _site).
"""

# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "jinja2==3.1.3",
#     "fire==0.7.0",
#     "loguru==0.7.0"
# ]
# ///
from typing import List, Union
from pathlib import Path
import json
import os
import shutil
import subprocess

import fire
import jinja2
from loguru import logger


def _generate_app_shell(
    output_dir: Path,
    shell_template_file: Path,
    shell_output_path: Path,
    title: str,
    embedded_path: str,
    nav_items: List[dict] | None = None,
    current_html_path: str = "",
) -> bool:
    """Generate a Tailwind wrapper page that embeds an exported app."""
    try:
        env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(str(shell_template_file.parent)),
            autoescape=jinja2.select_autoescape(["html", "xml"]),
        )
        template = env.get_template(shell_template_file.name)
        rendered = template.render(
            title=title,
            embedded_path=embedded_path,
            nav_items=nav_items or [],
            current_html_path=current_html_path,
        )

        out_path = output_dir / shell_output_path
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(rendered, encoding="utf-8")
        logger.info(f"Generated app shell: {out_path}")
        return True
    except IOError as e:
        logger.error(f"Failed writing shell page {shell_output_path}: {e}")
        return False
    except jinja2.exceptions.TemplateError as e:
        logger.error(f"Template rendering failed for {shell_template_file}: {e}")
        return False


def _load_apps_nav(nav_file: Path) -> List[dict]:
    """Load flat app navigation config from JSON.

    Supported list entries:
    - "apps/charts.py"
    - {"path": "apps/charts.py", "label": "Charts"}
    """
    if not nav_file.exists():
        logger.warning(f"Apps nav file not found: {nav_file}; using discovered app order")
        return []

    try:
        raw = json.loads(nav_file.read_text(encoding="utf-8"))
    except Exception as e:
        logger.error(f"Failed reading/parsing nav file {nav_file}: {e}")
        return []

    if not isinstance(raw, list):
        logger.error(f"Apps nav file must contain a JSON list: {nav_file}")
        return []

    entries: List[dict] = []
    for i, item in enumerate(raw):
        if isinstance(item, str):
            p = Path(item).as_posix()
            entries.append(
                {
                    "source_path": p,
                    "display_name": Path(p).stem.replace("_", " ").title(),
                }
            )
            continue

        if isinstance(item, dict):
            path_val = item.get("path")
            if not isinstance(path_val, str) or not path_val.strip():
                logger.warning(f"Skipping nav entry #{i}: missing/invalid 'path'")
                continue
            p = Path(path_val).as_posix()
            label = item.get("label")
            display_name = label if isinstance(label, str) and label.strip() else Path(p).stem.replace("_", " ").title()
            entries.append({"source_path": p, "display_name": display_name})
            continue

        logger.warning(f"Skipping nav entry #{i}: expected string or object, got {type(item).__name__}")

    return entries


def _build_apps_sidenav(apps_data: List[dict], nav_entries: List[dict]) -> List[dict]:
    """Order/filter app nav using JSON entries.

    - Apps not listed in JSON are hidden.
    - Missing JSON entries warn and continue.
    """
    if not nav_entries:
        return apps_data

    by_source = {app["source_path"]: app for app in apps_data}
    ordered: List[dict] = []

    for entry in nav_entries:
        src = entry["source_path"]
        app = by_source.get(src)
        if not app:
            logger.warning(f"Nav entry not found among exported apps: {src}")
            continue

        merged = dict(app)
        merged["display_name"] = entry.get("display_name", app["display_name"])
        ordered.append(merged)

    return ordered


def _relative_href(from_page: str, to_page: str) -> str:
    """Compute a relative href from one generated HTML page to another."""
    from_parent = Path(from_page).parent
    return Path(os.path.relpath(to_page, start=from_parent)).as_posix()


def _export_html_wasm(app_path: Path, output_dir: Path) -> bool:
    """Export a single marimo app to HTML/WebAssembly format."""
    output_path: Path = output_dir / app_path.with_name(f"{app_path.stem}_iframe.html")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    cmd: List[str] = [
        "uvx",
        "marimo",
        "export",
        "html-wasm",
        "--sandbox",
        "--mode",
        "run",
        "--no-show-code",
        str(app_path),
        "-o",
        str(output_path),
    ]

    logger.info(f"Exporting {app_path} -> {output_path}")
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Export failed for {app_path}: {e}")
        if e.stderr:
            logger.error(e.stderr.strip())
        return False
    except Exception as e:
        logger.error(f"Unexpected export error for {app_path}: {e}")
        return False


def _generate_index_redirect(output_dir: Path, target_href: str) -> None:
    """Generate index.html that redirects to the provided app shell page."""
    logger.info(f"Generating index.html redirect to {target_href}")

    index_path: Path = output_dir / "index.html"
    output_dir.mkdir(parents=True, exist_ok=True)

    redirect_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta http-equiv="refresh" content="0; url={target_href}" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Redirecting...</title>
  <script>window.location.replace({json.dumps(target_href)});</script>
</head>
<body>
  <p>Redirecting to <a href="{target_href}">{target_href}</a>...</p>
</body>
</html>
"""

    try:
        index_path.write_text(redirect_html, encoding="utf-8")
    except IOError as e:
        logger.error(f"Failed to write redirect index.html: {e}")


def _copy_static_assets(output_dir: Path) -> None:
    """Copy static assets needed by exported HTML files."""
    logger.info("Copying static assets")

    asset_paths: List[Path] = [
        Path("custom.css"),
        Path("head.html"),
        Path("apps/public"),
    ]

    for src in asset_paths:
        if not src.exists():
            logger.warning(f"Static asset not found, skipping: {src}")
            continue

        dst = output_dir / src
        try:
            if src.is_dir():
                if dst.exists():
                    shutil.rmtree(dst)
                shutil.copytree(src, dst)
                logger.info(f"Copied directory: {src} -> {dst}")
            else:
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)
                logger.info(f"Copied file: {src} -> {dst}")
        except Exception as e:
            logger.error(f"Failed copying asset {src}: {e}")


def _export(folder: Path, output_dir: Path) -> List[dict]:
    """Export all marimo apps in a folder to HTML/WebAssembly format."""
    if not folder.exists():
        logger.error(f"Apps folder does not exist: {folder}")
        return []

    app_files = sorted(
        p for p in folder.rglob("*.py")
        if "public" not in p.parts and p.name != "__init__.py"
    )
    logger.debug(f"Found {len(app_files)} app Python files in {folder}")

    if not app_files:
        logger.warning(f"No app files found in {folder}")
        return []

    app_data: List[dict] = []

    for app_file in app_files:
        if _export_html_wasm(app_file, output_dir):
            app_data.append(
                {
                    "source_path": app_file.as_posix(),
                    "display_name": app_file.stem.replace("_", " ").title(),
                    "html_path": app_file.with_name(f"{app_file.stem}_iframe.html").as_posix(),
                    "shell_path": app_file.with_suffix(".html").as_posix(),
                }
            )

    logger.info(f"Successfully exported {len(app_data)} out of {len(app_files)} files from {folder}")
    return app_data


def main(
    output_dir: Union[str, Path] = "_site",
    app_shell_template: Union[str, Path] = "templates/app_shell.html.j2",
    apps_nav_json: Union[str, Path] = "templates/apps_nav.json",
) -> None:
    """Main function to export marimo apps and generate app shells + redirect index."""
    logger.info("Starting marimo app build process")

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    shell_template_file = Path(app_shell_template)
    apps_nav_file = Path(apps_nav_json)

    _copy_static_assets(output_dir)

    apps_data = _export(Path("apps"), output_dir)
    if not apps_data:
        logger.warning("No apps exported. Skipping shell generation.")
        return

    nav_entries = _load_apps_nav(apps_nav_file)
    sidenav_apps = _build_apps_sidenav(apps_data, nav_entries)
    if not sidenav_apps:
        logger.warning("No apps in sidenav after nav filtering. Skipping shell generation.")
        return

    generated = 0
    for current in sidenav_apps:
        current_shell = current["shell_path"]
        embedded_path = _relative_href(current_shell, current["html_path"])

        nav_items = [
            {
                "display_name": item["display_name"],
                "html_path": _relative_href(current_shell, item["shell_path"]),
            }
            for item in sidenav_apps
        ]
        current_href = _relative_href(current_shell, current_shell)

        ok = _generate_app_shell(
            output_dir=output_dir,
            shell_template_file=shell_template_file,
            shell_output_path=Path(current_shell),
            title=current["display_name"],
            embedded_path=embedded_path,
            nav_items=nav_items,
            current_html_path=current_href,
        )
        generated += int(ok)

    if generated > 0:
        _generate_index_redirect(output_dir, sidenav_apps[0]["shell_path"])
        logger.info("Build completed successfully")
    else:
        logger.error("No shell pages were generated")


if __name__ == "__main__":
    fire.Fire(main)