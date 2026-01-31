from pathlib import Path

from core.project_loader import SoapUIProjectLoader
from core.testcase_extractor import TestCaseExtractor
from core.testcase_validator import TestCaseValidatorSummarizer
from core.script_reference_resolver import ScriptReferenceResolver
from core.project_aggregator import ProjectAggregator


def main():
    # 1️⃣ Load SoapUI project
    loader = SoapUIProjectLoader("input/soapui_project.xml")
    root = loader.load()

    # 2️⃣ Extract test suites & test cases
    suites = TestCaseExtractor(root).extract()

    # 3️⃣ Initialize helpers
    summarizer = TestCaseValidatorSummarizer()
    resolver = ScriptReferenceResolver(scripts_root=Path("input"))
    aggregator = ProjectAggregator()

    # ============================
    # TEST CASE–LEVEL DETAILS
    # ============================
    for suite in suites:
        print(f"\n============================")
        print(f"TestSuite: {suite.name}")
        print(f"============================")

        for tc in suite.test_cases:
            print(f"\n  TestCase: {tc.name}")
            print(f"  Enabled: {tc.enabled}")

            # Validations
            validations = summarizer.summarize(tc)
            if validations:
                print("  Validations:")
                for v in validations:
                    print(f"    - {v}")

            # External scripts
            if tc.external_scripts:
                print("  External Scripts:")
                intents = resolver.resolve(tc.external_scripts)
                for script, intent in intents.items():
                    print(f"    - {script} → {intent}")

    # ============================
    # PROJECT-LEVEL SUMMARY
    # ============================
    project_summary = aggregator.aggregate(suites)

    print("\n============================")
    print("PROJECT SUMMARY")
    print("============================")

    for key, value in project_summary.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
