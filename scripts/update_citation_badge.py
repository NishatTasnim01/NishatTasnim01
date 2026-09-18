"""
Regenerates a Google Scholar citation-count badge (SVG) for this profile.
"""

import os
import sys

import requests

# The "user=" value from the Scholar profile URL
AUTHOR_ID = "GBP9LAMAAAAJ"

OUTPUT_SVG = "citation_badge.svg"

# Matches the README's accent color
BADGE_COLOR = "#2E86DE"
LABEL_COLOR = "#555555"


def fetch_citation_count(author_id: str, api_key: str) -> int:
    response = requests.get(
        "https://serpapi.com/search",
        params={
            "engine": "google_scholar_author",
            "author_id": author_id,
            "api_key": api_key,
        },
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()

    status = data.get("search_metadata", {}).get("status")
    if status != "Success":
        raise RuntimeError(f"SerpApi search did not succeed: {data.get('search_metadata')}")

    try:
        return int(data["cited_by"]["table"][0]["citations"]["all"])
    except (KeyError, IndexError, ValueError) as exc:
        raise RuntimeError(f"Unexpected SerpApi response shape: {data}") from exc


def render_badge_svg(label: str, value: str) -> str:
    # Rough monospace-ish width estimate per character, close enough for a
    # small text badge -- avoids pulling in a font-metrics library.
    char_width = 6.5
    pad = 10
    label_width = int(len(label) * char_width + pad * 2)
    value_width = int(len(value) * char_width + pad * 2)
    total_width = label_width + value_width

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{total_width}" height="20">
  <rect width="{label_width}" height="20" fill="{LABEL_COLOR}"/>
  <rect x="{label_width}" width="{value_width}" height="20" fill="{BADGE_COLOR}"/>
  <g fill="#fff" text-anchor="middle" font-family="Verdana,Geneva,sans-serif" font-size="11">
    <text x="{label_width / 2}" y="14">{label}</text>
    <text x="{label_width + value_width / 2}" y="14">{value}</text>
  </g>
</svg>"""


def main() -> None:
    api_key = os.environ.get("SERPAPI_API_KEY")
    if not api_key:
        print("SERPAPI_API_KEY is not set.", file=sys.stderr)
        sys.exit(1)

    citation_count = fetch_citation_count(AUTHOR_ID, api_key)
    print(f"Fetched current citation count: {citation_count}")

    svg = render_badge_svg("CITATIONS", str(citation_count))
    with open(OUTPUT_SVG, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Wrote badge to {OUTPUT_SVG}")


if __name__ == "__main__":
    main()
