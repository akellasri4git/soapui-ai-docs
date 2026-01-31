from typing import List
from lxml import etree

from models.assertion_model import AssertionModel


class AssertionExtractor:
    """
    Extracts assertions from a SoapUI TestStep.
    """

    def __init__(self, teststep_element: etree._Element):
        self.teststep_element = teststep_element

    def extract(self) -> List[AssertionModel]:
        assertions: List[AssertionModel] = []

        assertion_elements = self.teststep_element.xpath(
            ".//con:assertion",
            namespaces=self.teststep_element.nsmap
        )

        for assertion in assertion_elements:
            name = assertion.get("name", "UnnamedAssertion")
            assertion_type = assertion.get("type", "unknown")
            enabled_attr = assertion.get("enabled", "true")

            expected = self._get_text(assertion, "con:expected")
            path = self._get_text(assertion, "con:path")

            # Normalize operator meaning
            operator = self._infer_operator(assertion_type)

            model = AssertionModel(
                name=name,
                type=assertion_type,
                enabled=(enabled_attr.lower() != "false"),
                expected=expected or path,
                operator=operator
            )

            assertions.append(model)

        return assertions

    def _get_text(self, element: etree._Element, tag: str) -> str | None:
        el = element.find(tag, namespaces=element.nsmap)
        return el.text.strip() if el is not None and el.text else None

    def _infer_operator(self, assertion_type: str) -> str:
        """
        Converts SoapUI assertion types into semantic operators.
        """
        mapping = {
            "JsonPath Match": "PRESENT",
            "XPath Match": "PRESENT",
            "Valid HTTP Status Codes": "EQUALS",
            "Not Contains": "NOT_PRESENT",
            "Contains": "PRESENT",
            "Response SLA": "LESS_THAN"
        }
        return mapping.get(assertion_type, "UNKNOWN")
