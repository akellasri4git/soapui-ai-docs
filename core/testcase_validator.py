from typing import List

from models.testcase_model import TestCaseModel
from models.assertion_model import AssertionModel


class TestCaseValidatorSummarizer:
    """
    Converts assertions into human-readable validation summaries
    per TestCase.
    """

    def summarize(self, testcase: TestCaseModel) -> List[str]:
        validations: List[str] = []

        for step in testcase.test_steps:
            for assertion in step.assertions:
                sentence = self._assertion_to_sentence(assertion)
                if sentence:
                    validations.append(sentence)

        return validations

    # -------------------------
    # Assertion → Sentence
    # -------------------------
    def _assertion_to_sentence(self, assertion: AssertionModel) -> str | None:
        if not assertion.enabled:
            return None

        operator = assertion.operator
        expected = assertion.expected

        if operator == "EQUALS":
            return f"Response value must equal `{expected}`"

        if operator == "PRESENT":
            return f"`{expected}` must be present in the response"

        if operator == "NOT_PRESENT":
            return f"`{expected}` must NOT be present in the response"

        if operator == "LESS_THAN":
            return f"Response time must be less than `{expected}`"

        return f"Validates assertion `{assertion.name}`"
