"""Fetch the OpenFarmPlanner public library (crops, species, families, plant health) into a dated JSON snapshot.

Uses your own login session (the list endpoint needs one). Credentials come from env vars:
  OFP_EMAIL + OFP_PASSWORD   (email/password account), or
  OFP_SESSIONID              (the `sessionid` cookie copied from the browser, e.g. Google login)

  uv run tools/pull_public_library.py --base https://openfarmplanner.org --pages 1
  uv run tools/pull_public_library.py --base http://localhost:8000            # all pages

Data is CC BY-SA 4.0: keep `license` and `attribution` with the snapshot.
"""

import argparse
import datetime
import http.cookiejar
import json
import os
import time
import urllib.parse
import urllib.error
import urllib.request

parser = argparse.ArgumentParser()
parser.add_argument("--base", default="https://openfarmplanner.org")
parser.add_argument("--pages", type=int, default=0, help="0 = all")
parser.add_argument("--out", default="public_crops_snapshot.json")
args = parser.parse_args()

jar = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
opener.addheaders = [("User-Agent", "ofp-library-snapshot/0.1"), ("Referer", args.base + "/")]
api = args.base.rstrip("/") + "/api"


def get(url):
    with opener.open(url, timeout=30) as r:
        return json.load(r)


if os.environ.get("OFP_SESSIONID"):
    host = urllib.parse.urlparse(args.base).hostname
    jar.set_cookie(http.cookiejar.Cookie(0, "sessionid", os.environ["OFP_SESSIONID"], None, False, host, False,
                                         False, "/", True, False, None, False, None, None, {}))
else:
    opener.open(api + "/auth/csrf/", timeout=30).read()
    csrf = next(c.value for c in jar if c.name == "csrftoken")
    body = json.dumps({"email": os.environ["OFP_EMAIL"], "password": os.environ["OFP_PASSWORD"]}).encode()
    req = urllib.request.Request(api + "/auth/login/", body, {"Content-Type": "application/json", "X-CSRFToken": csrf})
    opener.open(req, timeout=30).read()

ENDPOINTS = ["public-crops", "crop-species", "plant-families", "plant-health/entries", "plant-health/hosts"]


def fetch_all(endpoint):
    url, rows, page = f"{api}/{endpoint}/?page_size=100", [], 0
    while url and (args.pages == 0 or page < args.pages):
        data = get(url)
        if isinstance(data, list):  # unpaginated endpoint
            return data
        rows += data["results"]
        url, page = data["next"], page + 1
        print(f"{endpoint} page {page}: {len(rows)}/{data['count']}")
        time.sleep(1)  # be polite to a donation-funded server
    return rows


sections = {}
for endpoint in ENDPOINTS:
    try:
        sections[endpoint] = fetch_all(endpoint)
    except urllib.error.HTTPError as e:
        print(f"{endpoint}: HTTP {e.code}, skipped")

snapshot = {
    "source": args.base,
    "fetched_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "license": "CC BY-SA 4.0 (https://creativecommons.org/licenses/by-sa/4.0/)",
    "attribution": "OpenFarmPlanner community crop library contributors",
    "counts": {k: len(v) for k, v in sections.items()},
    **sections,
}
with open(args.out, "w", encoding="utf-8") as f:
    json.dump(snapshot, f, ensure_ascii=False, indent=1)
print(f"wrote {snapshot['counts']} to {args.out}")
