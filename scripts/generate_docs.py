import json
from core.logger import setup_logger
from core.llm_client import LLMClient
from core.documentation_generator import DocumentationGenerator

logger = setup_logger("Runner")


def main():
    logger.info("===== SoapUI AI Documentation Generator STARTED =====")

    enriched_project = json.load(
        open("output/project_enriched.json", "r", encoding="utf-8")
    )

    llm = LLMClient(model="llama3.1:8b")
    generator = DocumentationGenerator(llm)

    documentation = generator.generate(enriched_project)

    with open("output/soapui_documentation.md", "w", encoding="utf-8") as f:
        f.write(documentation)

    logger.info("Documentation written to output/soapui_documentation.md")
    logger.info("===== PROCESS COMPLETED SUCCESSFULLY =====")


if __name__ == "__main__":
    main()
