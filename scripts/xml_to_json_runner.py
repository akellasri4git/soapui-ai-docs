from core.xml_to_json import XMLToJSONConverter
from core.json_enricher import JSONStructureEnricher
from core.json_filter import JSONSemanticFilter
import json
from pathlib import Path


def main():
    # Step 1: XML → JSON
    xml_converter = XMLToJSONConverter("input/small_soapui_project.xml")
    raw_json = xml_converter.convert()

    # Step 2: Enrich structure
    enricher = JSONStructureEnricher()
    structured_json = enricher.enrich(raw_json)

    # Step 3: Semantic filtering
    semantic_filter = JSONSemanticFilter()
    filtered_json = semantic_filter.filter(structured_json)

    output_path = Path("output/project_llm_ready.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(filtered_json, f, indent=2, ensure_ascii=False)

    print("✅ XML → JSON → Structured → LLM-Ready JSON completed")


if __name__ == "__main__":
    main()
