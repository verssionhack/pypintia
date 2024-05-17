from enum import Enum
from typing import Any, List
from dataclasses import dataclass
from dataclasses_json import dataclass_json
import json as j

class ProblemSubmissionStatus(Enum):
    ACCEPTED = 'PROBLEM_ACCEPTED'

class ProblemType(Enum):
    COMPLETION = 'CODE_COMPLETION'

@dataclass
class ProblemStatus:
    id: str
    label: str
    score: int
    problem_submission_status: str
    problem_type: str
    problem_pool_index: int
    index_in_problem_pool: int

    def __init__(self, data: dict):
        self.id = data.get('id')
        self.label = data.get('label')
        self.score = data.get('score')
        self.problem_submission_status = data.get('problem_submission_status')
        self.problem_type = data.get('problem_type')
        self.problem_pool_index = data.get('problem_pool_index')
        self.index_in_problem_pool = data.get('index_in_problem_pool')

@dataclass
class ProblemStatusPacket:
    problem_status: List[ProblemStatus]

    def __init__(self, data: dict):
        self.problem_status = [ProblemStatus(i) for i in (data.get('problem_status') if data.get('problem_status') != None else [])]
