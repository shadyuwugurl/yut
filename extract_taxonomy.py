#!/usr/bin/env python3
"""extract_taxonomy.py — single source of truth for the Sharp-Spark taxonomy.

Parses the valid lists straight out of the chat template and emits taxonomy.json.
Point build_queue.py and the decision-head training labels at this JSON so the
queue and the router can never drift from the template again.

Usage:
    python3 extract_taxonomy.py Sharp-Spark_v5.0.1.jinja taxonomy.json
"""
import ast, json, re, sys
from pathlib import Path

EXPECTED = {"modes": 25, "constructs": 30, "personas": 20, "identities": 33, "themes": 8}
NON_VALUES = {"modes": {"auto"}, "constructs": set(), "personas": {"neutral"},
              "identities": {"none"}, "themes": {"none"}}
LISTS = {"_valid_modes": "modes", "_valid_construct": "constructs",
         "_valid_persona": "personas", "_valid_identity": "identities",
         "_valid_theme": "themes"}

def main(tpl_path, out_path):
    src = Path(tpl_path).read_text()
    out, ok = {}, True
    for lst, key in LISTS.items():
        m = re.search(re.escape(lst) + r"\s*=\s*(\[[^\]]*\])", src)
        if not m:
            sys.exit(f"could not find {lst} in {tpl_path}")
        items = ast.literal_eval(m.group(1))
        values = [i for i in items if i not in NON_VALUES[key]]
        out[key] = {"count": len(values), "values": values, "all": items}
        mark = "OK " if len(values) == EXPECTED[key] else "MISMATCH"
        if len(values) != EXPECTED[key]:
            ok = False
        print(f"{mark} {key}: {len(values)} (expected {EXPECTED[key]})")
    doc = {"taxonomy": "v0.3", "source": Path(tpl_path).name, **out}
    Path(out_path).write_text(json.dumps(doc, indent=2) + "\n")
    print(f"wrote {out_path}")
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "Sharp-Spark_v5.0.1.jinja",
         sys.argv[2] if len(sys.argv) > 2 else "taxonomy.json")
