#!/usr/bin/env python3
"""Inline practice.json into built preview HTML and remove runtime JSON dependency."""

from __future__ import annotations

import json
from pathlib import Path


LOAD_CONFIG_SNIPPET = """    async function loadPracticeConfig() {
      const response = await fetch('./practice.json');
      if (!response.ok) throw new Error(`Unable to load practice.json: ${response.status}`);
      return response.json();
    }
"""

RENDER_SNIPPET = """    loadPracticeConfig()
      .then(FrontdoorHome.render)
      .catch((error) => {
        console.error(error);
        document.getElementById('app').innerHTML = '<main class="page-shell py-20"><h1 class="text-3xl font-semibold text-slate-950">Unable to load site content.</h1><p class="mt-4 text-slate-600">Please try again later.</p></main>';
      });
"""


def embed_practice_config(practice_dir: Path) -> None:
    index_path = practice_dir / "index.html"
    json_path = practice_dir / "practice.json"

    if not index_path.exists() or not json_path.exists():
        return

    config = json.loads(json_path.read_text())
    config_js = json.dumps(config, ensure_ascii=False, indent=6)
    html = index_path.read_text()

    if LOAD_CONFIG_SNIPPET not in html:
        raise ValueError(f"Missing loadPracticeConfig snippet in {index_path}")
    if RENDER_SNIPPET not in html:
        raise ValueError(f"Missing render snippet in {index_path}")

    html = html.replace(
        LOAD_CONFIG_SNIPPET,
        f"    const practiceConfig = {config_js};\n",
    )
    html = html.replace(RENDER_SNIPPET, "    FrontdoorHome.render(practiceConfig);\n")

    index_path.write_text(html)
    json_path.unlink()


def main() -> None:
    dist = Path("dist")
    for practice_dir in dist.iterdir():
        if practice_dir.is_dir():
            embed_practice_config(practice_dir)


if __name__ == "__main__":
    main()
