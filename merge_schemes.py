"""Merge new_schemes.json into schemes.json, skipping duplicate IDs."""
import json, os, sys

base = os.path.dirname(os.path.abspath(__file__))
orig_path = os.path.join(base, 'data', 'schemes.json')
new_path  = os.path.join(base, 'data', 'new_schemes.json')
out_path  = orig_path

if not os.path.exists(new_path):
    print("new_schemes.json not found — nothing to merge.")
    sys.exit(0)

with open(orig_path, encoding='utf-8') as f:
    orig = json.load(f)
with open(new_path, encoding='utf-8') as f:
    new  = json.load(f)

existing_ids = {s['id'] for s in orig}
added = 0
for s in new:
    if s['id'] not in existing_ids:
        orig.append(s)
        existing_ids.add(s['id'])
        added += 1
    else:
        print(f"  skip duplicate: {s['id']}")

with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(orig, f, ensure_ascii=False, indent=2)

print(f"\nDone. Added {added} new schemes. Total: {len(orig)}")
