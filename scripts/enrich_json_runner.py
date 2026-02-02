from core.logger import setup_logger
from core.json_enricher import JSONStructureEnricher
import json
from pathlib import Path

logger = setup_logger("EnricherRunner")


def main():
    logger.info("Starting JSON enrichment")

    input_path = Path("output/project_raw.json")
    output_path = Path("output/project_enriched.json")

    if not input_path.exists():
        raise FileNotFoundError("project_raw.json not found. Run xml_to_json first.")

    raw_json = json.loads(input_path.read_text(encoding="utf-8"))

    enricher = JSONStructureEnricher()
    enriched = enricher.enrich(raw_json)

    output_path.write_text(
        json.dumps(enriched, indent=2),
        encoding="utf-8"
    )

    logger.info("Enriched JSON written to output/project_enriched.json")


if __name__ == "__main__":
    main()
