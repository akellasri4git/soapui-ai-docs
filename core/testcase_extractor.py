from typing import List
from lxml import etree

from utils.xml_utils import find_elements
from models.testsuite_model import TestSuiteModel
from models.testcase_model import TestCaseModel
from core.teststep_extractor import TestStepExtractor


class TestCaseExtractor:
    """
    Extracts TestSuites and TestCases from SoapUI XML.
    """

    def __init__(self, root: etree._Element):
        self.root = root

    def extract(self) -> List[TestSuiteModel]:
        test_suites: List[TestSuiteModel] = []

        suite_elements = find_elements(
            self.root,
            "//con:testSuite"
        )

        for suite in suite_elements:
            suite_name = suite.get("name", "UnnamedTestSuite")

            test_cases: List[TestCaseModel] = []

            case_elements = suite.xpath(
                ".//con:testCase",
                namespaces=self.root.nsmap
            )

            for case in case_elements:
                case_name = case.get("name", "UnnamedTestCase")
                disabled_attr = case.get("disabled", "false")

                step_extractor = TestStepExtractor(case)
                test_steps = step_extractor.extract()
                external_scripts = []

                for step in test_steps:
                    if step.external_scripts:
                        external_scripts.extend(step.external_scripts)

                test_case = TestCaseModel(
                    name=case_name,
                    enabled=(disabled_attr.lower() != "true"),
                    test_steps=test_steps,
                    external_scripts=list(set(external_scripts))
                )


                test_cases.append(test_case)

            test_suites.append(
                TestSuiteModel(
                    name=suite_name,
                    test_cases=test_cases
                )
            )

        return test_suites
