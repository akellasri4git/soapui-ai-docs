from pydantic import BaseModel
from typing import List
from models.teststep_model import TestStepModel


class TestCaseModel(BaseModel):
    name: str
    enabled: bool

    test_steps: List[TestStepModel] = []

    external_scripts: List[str] = []
