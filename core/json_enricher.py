"""
JSON structural enricher.

Adds:
- Unique node IDs
- Stable structural paths

NO interpretation
NO SoapUI assumptions
"""

from typing import Dict, Any
from copy import deepcopy


class JSONStructureEnricher:
    def __init__(self):
        self._counter = 0

    def enrich(self, data: Dict[str, Any]) -> Dict[str, Any]:
        enriched = deepcopy(data)
        self._walk(enriched["root"], path="/root")
        return enriched

    def _walk(self, node: Dict[str, Any], path: str):
        self._counter += 1

        node["id"] = f"node_{self._counter:06d}"
        node["path"] = path

        for index, child in enumerate(node.get("children", [])):
            child_path = f"{path}/children[{index}]"
            self._walk(child, child_path)
