
#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
from pathlib import Path
from html import escape


HTML = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,height=device-height,initial-scale=1" />
  <title>{title}</title>
  <style>
    html, body {{
      width: 100%;
      height: 100%;
      margin: 0;
      padding: 0;
      overflow: hidden;
      background: #0000;
    }}
    /* Full-bleed PDF */
    object {{
      width: 100vw;
      height: 100vh;
      border: 0;
      display: block;
    }}
  </style>
</head>
<body>
  <object data="{pdf_href}" type="application/pdf">
    <!-- Fallback if embedding is disabled -->
    <a href="{pdf_href}">{pdf_href}</a>
  </object>
</body>
</html>
"""


def repo_name_from_env() -> str:
    """
    GitHub Actions provides GITHUB_REPOSITORY="owner/repo".
    Locally this may be missing, so we fall back to "Document".
    """
    gh_repo = os.environ.get("GITHUB_REPOSITORY", "").strip()
    if "/" in gh_repo:
        return gh_repo.split("/", 1)[1]
    return "Document"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True, help="Output HTML path (e.g. dist/index.html)")
    ap.add_argument("--pdf", required=True, help="PDF href relative to the HTML (e.g. document.pdf)")
    ap.add_argument("--title", default="", help="HTML title. If empty, uses repo name when available.")
    args = ap.parse_args()

    title = args.title.strip() or repo_name_from_env()

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)

    html = HTML.format(
      title=escape(title),
      pdf_href=escape(args.pdf),
    )
    out.write_text(html, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
