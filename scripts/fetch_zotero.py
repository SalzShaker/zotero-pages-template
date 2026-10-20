"""Fetch a Zotero library and save it as JSON for the website.

Runs in GitHub Actions (see .github/workflows/zotero.yml) or on your computer:
    ZOTERO_API_KEY=... python scripts/fetch_zotero.py

Settings are read from config.js (libraryType, libraryId, collectionKey, style, maxItems),
so there is only one place to configure the site. The API key comes from the
environment variable ZOTERO_API_KEY – never from a file in the repository.
Writes data/items.json and data/notes.json. Standard library only.
"""
import json, os, re, sys, time, urllib.parse, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
API = "https://api.zotero.org"


def read_config():
    text = (ROOT / "config.js").read_text(encoding="utf-8")
    def get(name, default=""):
        m = re.search(rf'^\s*{name}\s*:\s*(?:"([^"]*)"|(\d+)|(true|false))', text, re.M)
        if not m:
            return default
        return m.group(1) if m.group(1) is not None else (m.group(2) or m.group(3))
    return {"libraryType": get("libraryType", "groups"), "libraryId": get("libraryId"),
            "collectionKey": get("collectionKey"), "style": get("style", "chicago-author-date"),
            "maxItems": int(get("maxItems", "500"))}


def get_all(url, params, key, max_items):
    """Pagination: limit=100, start=0, 100, 200 … until Total-Results is reached."""
    items, start, total = [], 0, None
    while (total is None or start < total) and start < max_items:
        q = urllib.parse.urlencode({**params, "limit": 100, "start": start})
        req = urllib.request.Request(f"{url}?{q}", headers={"Zotero-API-Version": "3"})
        if key:
            req.add_header("Zotero-API-Key", key)
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                total = int(r.headers.get("Total-Results", "0"))
                wait = r.headers.get("Backoff") or r.headers.get("Retry-After")
                items += json.load(r)
        except urllib.error.HTTPError as e:
            sys.exit(f"Zotero API answered {e.code} {e.reason} for {url}\n"
                     "403: key missing or without access · 404: wrong libraryId/collectionKey")
        start += 100
        print(f"  {len(items)} of {total}")
        time.sleep(int(wait) if wait else 1)          # be a considerate client
    return items


def main():
    c = read_config()
    key = os.environ.get("ZOTERO_API_KEY", "").strip()
    base = f"{API}/{c['libraryType']}/{c['libraryId']}"
    scope = f"{base}/collections/{c['collectionKey']}" if c["collectionKey"] else base
    print(f"Library {c['libraryType']}/{c['libraryId']} collection={c['collectionKey'] or '(all)'} "
          f"key={'yes' if key else 'no'}")

    items = get_all(f"{scope}/items/top", {"include": "bib,data", "style": c["style"], "sort": "creator"},
                    key, c["maxItems"])
    notes = get_all(f"{base}/items", {"itemType": "note"}, key, 1000)
    # keep only what the page needs – no library metadata, no user names
    items = [{"key": i["key"], "bib": i.get("bib", ""), "meta": {"parsedDate": i.get("meta", {}).get("parsedDate", "")},
              "data": {k: i["data"].get(k) for k in ("itemType", "title", "date", "tags", "creators")}} for i in items]
    # only notes that belong to items shown on the page – everything in data/ becomes public
    shown = {i["key"] for i in items}
    notes = [{"data": {"parentItem": n["data"]["parentItem"], "note": n["data"].get("note", "")}}
             for n in notes if n["data"].get("parentItem") in shown]

    out = ROOT / "data"
    out.mkdir(exist_ok=True)
    (out / "items.json").write_text(json.dumps(items, ensure_ascii=False, indent=1), encoding="utf-8")
    (out / "notes.json").write_text(json.dumps(notes, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"Saved {len(items)} items and {len(notes)} notes to data/")


if __name__ == "__main__":
    main()
