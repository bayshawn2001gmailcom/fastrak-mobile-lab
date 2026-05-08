"""
Detect and collapse redirect chains on fastrakmobilelab.com.
Uses Rank Math redirection API to find A->B->C chains and collapse to A->C.

Usage:
  python tools/redirect_fixer.py --dry-run    # preview only, no changes
  python tools/redirect_fixer.py              # apply fixes
"""
import os, sys, argparse, requests, base64, json, time
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
load_dotenv(Path.home() / ".env", override=False)

WP_SITE = os.getenv("WP_SITE", "https://fastrakmobilelab.com").rstrip("/")
WP_USER = os.getenv("WP_USER")
WP_APP_PASSWORD = os.getenv("WP_APP_PASSWORD")

if not WP_USER or not WP_APP_PASSWORD:
    sys.exit("Error: WP_USER and WP_APP_PASSWORD must be set in ~/.env")

creds = base64.b64encode(f"{WP_USER}:{WP_APP_PASSWORD}".encode()).decode()
HEADERS = {"Authorization": f"Basic {creds}", "Content-Type": "application/json"}
SESSION = requests.Session()
SESSION.headers.update({"User-Agent": "FastrakSEOBot/1.0"})


def get_redirections():
    """Fetch all Rank Math redirections."""
    url = f"{WP_SITE}/wp-json/rankmath/v1/redirections"
    resp = SESSION.get(url, headers=HEADERS, timeout=20)
    resp.raise_for_status()
    return resp.json()


def resolve_final_destination(start_url, redirect_map, max_hops=10):
    """Follow the redirect chain from start_url to its final destination."""
    visited = [start_url]
    current = start_url
    for _ in range(max_hops):
        dest = redirect_map.get(current)
        if dest is None:
            break
        if dest in visited:
            return current, visited, True  # loop detected
        visited.append(dest)
        current = dest
    return current, visited, False


def detect_chains(redirections):
    """Build redirect map and identify chains longer than 1 hop."""
    redirect_map = {}
    for r in redirections:
        src = r.get("sources", [{}])[0].get("pattern", "")
        dst = r.get("destination", "")
        if src and dst:
            # Normalize to full URL if relative
            if src.startswith("/"):
                src = WP_SITE + src
            if dst.startswith("/"):
                dst = WP_SITE + dst
            redirect_map[src] = dst

    chains = []
    for start_url in redirect_map:
        final, hops, is_loop = resolve_final_destination(start_url, redirect_map)
        if len(hops) > 2:  # A->B->C or longer
            chains.append({
                "start": start_url,
                "final": final,
                "hops": hops,
                "is_loop": is_loop,
            })

    return chains, redirect_map


def patch_redirect(redirection_id, new_destination, dry_run=False):
    """Update a single redirection to point directly to the final destination."""
    if dry_run:
        return True
    url = f"{WP_SITE}/wp-json/rankmath/v1/redirections/{redirection_id}"
    resp = SESSION.patch(url, headers=HEADERS, json={"destination": new_destination}, timeout=20)
    return resp.ok


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without applying")
    args = parser.parse_args()

    mode = "[DRY RUN]" if args.dry_run else "[LIVE]"
    print(f"{mode} Fetching redirections from {WP_SITE}...")

    try:
        redirections = get_redirections()
    except Exception as e:
        sys.exit(f"Failed to fetch redirections: {e}")

    print(f"Found {len(redirections)} total redirections.")

    chains, redirect_map = detect_chains(redirections)

    if not chains:
        print("No redirect chains detected. All good.")
        return

    print(f"\nFound {len(chains)} redirect chain(s):\n")
    for chain in chains:
        hops_str = " -> ".join(chain["hops"])
        status = "[LOOP]" if chain["is_loop"] else f"[{len(chain['hops'])-1} hops]"
        print(f"  {status} {hops_str}")

    if args.dry_run:
        print(f"\n{mode} No changes made. Run without --dry-run to apply fixes.")
        return

    print("\nCollapsing chains...")
    fixed = 0
    for r in redirections:
        src = r.get("sources", [{}])[0].get("pattern", "")
        if src.startswith("/"):
            src = WP_SITE + src
        for chain in chains:
            if src == chain["start"] and not chain["is_loop"]:
                redirection_id = r.get("id")
                if patch_redirect(redirection_id, chain["final"]):
                    print(f"  [OK] {chain['start']} -> {chain['final']} (was {len(chain['hops'])-1} hops)")
                    fixed += 1
                else:
                    print(f"  [FAIL] Could not update redirection {redirection_id}")
                time.sleep(0.1)

    print(f"\nDone. {fixed} chain(s) collapsed.")


if __name__ == "__main__":
    main()
