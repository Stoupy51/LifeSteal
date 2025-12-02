
# Imports
import sys
import time
from typing import Any

import requests
import stouputils as stp

API: str = "https://api.modrinth.com/v2"
PROJECT_SLUG: str = "lifestealfr"

def get_project(project_slug: str) -> dict[str, Any]:
    r: requests.Response = requests.get(f"{API}/project/{project_slug}")
    r.raise_for_status()
    return r.json()

def get_versions(project_id: str) -> list[dict[str, Any]]:
    r: requests.Response = requests.get(f"{API}/project/{project_id}/version")
    r.raise_for_status()
    return r.json()

def get_version(version_id: str) -> dict[str, Any]:
    r: requests.Response = requests.get(f"{API}/version/{version_id}")
    r.raise_for_status()
    return r.json()

def search_modpacks_paginated(total: int = 1000, page_size: int = 100) -> list[dict[str, Any]]:
    """Fetch modpacks in pages of 100, sorted by update date (most recent first)."""
    all_hits: list[dict[str, Any]] = []
    url: str = f"{API}/search"

    for offset in stp.colored_for_loop(range(0, total, page_size), desc="Fetching modpacks"):
        params: dict[str, str | int] = {
            "query": "",
            "limit": page_size,
            "offset": offset,
            "index": "updated",   # sort by last update
            "sort": "desc",
            "facets": '[["project_type:modpack"]]'
        }

        r: requests.Response = requests.get(url, params=params)
        r.raise_for_status()
        data: dict[str, Any] = r.json()

        hits: list[dict[str, Any]] = data.get("hits", [])
        if not hits:
            break  # no more results

        all_hits.extend(hits)

        # Modrinth should return at most 100 hits per request; stop early if fewer
        if len(hits) < page_size:
            break

        time.sleep(0.2)

    return all_hits[:total]  # safety trim

def main() -> None:
    # Get total modpacks to fetch from command line argument, default to 100
    total_modpacks: int = 100
    if len(sys.argv) > 1:
        try:
            total_modpacks = int(sys.argv[1])
        except ValueError:
            stp.warning(f"Invalid argument '{sys.argv[1]}', using default value of 100")

    stp.info("Fetching LifeStealFR project...")
    project: dict[str, Any] = get_project(PROJECT_SLUG)
    project_id: str = project["id"]

    stp.info(f"Project ID = {project_id}")

    stp.info(f"Fetching up to {total_modpacks} modpacks (sorted by last update)...")
    modpacks: list[dict[str, Any]] = search_modpacks_paginated(total=total_modpacks, page_size=100)

    stp.info(f"Found {len(modpacks)} modpacks to inspect.")

    found_count: int = 0

    for mp in stp.colored_for_loop(modpacks, desc="Inspecting modpacks"):
        mp_id: str = mp["project_id"]
        mp_slug: str = mp["slug"]

        try:
            versions: list[dict[str, Any]] = get_versions(mp_id)
        except Exception as e:
            stp.warning(f"Error fetching versions for modpack {mp_slug}: {e}")
            continue

        for v in versions:
            for dep in v.get("dependencies", []):
                if dep.get("project_id") == project_id:
                    found_count += 1
                    stp.info(f"Found: {mp['title']} ({mp_slug}) | version={v['id']} | type={dep.get('dependency_type')}")
        time.sleep(0.1)

    if found_count == 0:
        stp.warning("Aucun modpack trouvé utilisant explicitement LifeStealFR.")
    else:
        stp.info(f"\nTotal modpacks using LifeStealFR: {found_count}")

if __name__ == "__main__":
    main()

