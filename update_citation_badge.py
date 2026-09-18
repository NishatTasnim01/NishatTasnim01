"""
Regenerates a Google Scholar citation-count badge (SVG) for this profile.

Why this exists:
Google Scholar has no official API, and shields.io can't query it directly.
This script uses the open-source `gsbg` (Google Scholar Badge Generator)
package to scrape the current total citation count from a Scholar profile
and render it as an SVG badge, which is then committed to the repo by the
accompanying GitHub Actions workflow on a schedule.

Run manually with:  pip install gsbg && python scripts/update_citation_badge.py
"""

import gsbg

# Nishat Tasnim's Google Scholar profile
SCHOLAR_PROFILE_URL = "https://scholar.google.com/citations?user=GBP9LAMAAAAJ&hl=en"

# Output path -- referenced directly by README.md via a raw.githubusercontent.com link
OUTPUT_SVG = "citation_badge.svg"


def main() -> None:
    citation_count = gsbg.fetch_profile_citation_num(SCHOLAR_PROFILE_URL)
    print(f"Fetched current citation count: {citation_count}")

    gsbg.gene_citation_badge_svg(
        link=SCHOLAR_PROFILE_URL,
        link_type="profile",
        svg_name=OUTPUT_SVG,
    )
    print(f"Wrote badge to {OUTPUT_SVG}")


if __name__ == "__main__":
    main()
