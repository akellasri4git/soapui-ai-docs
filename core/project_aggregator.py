from typing import Dict, Set

from models.testsuite_model import TestSuiteModel


class ProjectAggregator:
    """
    Aggregates project-level insights from extracted TestSuites.
    """

    def aggregate(self, suites: list[TestSuiteModel]) -> Dict:
        summary = {
            "test_suites_count": 0,
            "test_cases_total": 0,
            "test_cases_enabled": 0,
            "test_cases_disabled": 0,
            "unique_endpoints": set(),
            "unique_operations": set(),
            "unique_queues": set(),
            "external_scripts": set(),
        }

        summary["test_suites_count"] = len(suites)

        for suite in suites:
            for tc in suite.test_cases:
                summary["test_cases_total"] += 1

                if tc.enabled:
                    summary["test_cases_enabled"] += 1
                else:
                    summary["test_cases_disabled"] += 1

                # TestSteps
                for step in tc.test_steps:
                    if step.endpoint:
                        summary["unique_endpoints"].add(step.endpoint)

                    if step.operation:
                        summary["unique_operations"].add(step.operation)

                    if step.queue_name:
                        summary["unique_queues"].add(step.queue_name)

                # External scripts
                for script in tc.external_scripts:
                    summary["external_scripts"].add(script)

        # Convert sets to sorted lists for output
        return {
            "test_suites_count": summary["test_suites_count"],
            "test_cases_total": summary["test_cases_total"],
            "test_cases_enabled": summary["test_cases_enabled"],
            "test_cases_disabled": summary["test_cases_disabled"],
            "unique_endpoints": sorted(summary["unique_endpoints"]),
            "unique_operations": sorted(summary["unique_operations"]),
            "unique_queues": sorted(summary["unique_queues"]),
            "external_scripts": sorted(summary["external_scripts"]),
        }
