#!/usr/bin/env python3
"""All identity and theme specs, keyed by canonical id."""
from __future__ import annotations

from rest import SPECS_REST
from rest2 import SPECS_2
from rest3 import SPECS_3
from voices import PARTNER, YAOI, YURI

SPECS = {
    spec["id"]: spec
    for spec in [PARTNER, YAOI, YURI, *SPECS_REST, *SPECS_2, *SPECS_3]
}
SPECS["josie"] = {"id": "josie", "kind": "josie"}
