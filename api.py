HOST = 'pintia.cn'


import requests as r
from .user import UserPacket
from .profile import ProfilePacket
from .exams import Exams
from .problem_status import ProblemStatus
from .exam_problem import ExamProblem
from .problem_exam_list import ProblemExamList
from .problem_exam import ProblemExam
from .problem_exam_problem import ProblemExamProblem
from .last_submissions import LastSubmissions
from .problem_ranking import ProblemRanking
from .problem_types import ProblemTypes
from .problem_sets import ProblemSets
from .utils import dict_key2snake_name
import json as j


USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'

class Pintia:

    def __init__(self, cookies: dict[str, str]):
        self.cookies = cookies

        self.session = r.session()
        self.session.cookies.update(self.cookies)
        self.session.headers['user-agent'] = USER_AGENT
        self.session.headers['accept'] = 'application/json;charset=UTF-8'

        self.url = f'https://pintia.cn'


    def _get(self, uri: str, **args):
        ret = self.session.get(self.url + uri, **args)
        if ret.status_code != 200:
            print(f'status={ret.status_code} uri={uri}')
            print(f'response={ret.text}')
            input()
        try:
            ret_json = ret.json()
            dict_key2snake_name(ret_json)
            #print(j.dumps(ret_json, ensure_ascii=0, indent=4))
            return ret_json
        except Exception as e:
            print(f'error for {uri}: {e}')
            print(f'reply={ret.text}')
            input()


    def _post(self, uri: str, **args):
        ret = self.session.post(self.url + uri, **args)
        if ret.status_code != 200:
            print(f'status={ret.status_code} uri={uri}')
            print(f'response={ret.text}')
            input()
        try:
            ret_json = ret.json()
            dict_key2snake_name(ret_json)
            #print(j.dumps(ret_json, ensure_ascii=0, indent=4))
            return ret_json
        except Exception as e:
            print(f'error for {uri}: {e}')
            print(f'reply={ret.text}')
            input()

    def user_profile(self) -> UserPacket:
        uri = '/api/users/profile'
        return ProfilePacket(self._get(uri))

    def current_user(self) -> UserPacket:
        uri = '/api/u/current'
        return UserPacket(self._get(uri))

    def problem_sets(self, limit: int, filter='', order_by='', asc=True):
        uri = f'/api/problem-sets?filter={filter}&limit={limit}&order_by={order_by}&asc={str(asc).lower()}'
        return ProblemSets(self._get(uri))

    def problem_sets_exams(self, problem_sets_id: str):
        uri = f'/api/problem-sets/{problem_sets_id}/exams'
        return Exams(self._get(uri))

    def problem_sets_summaries(self, problem_sets_id: str):
        uri = f'/api/problem-sets/{problem_sets_id}/problem-summaries'
        pass

    def problem_sets_status(self, problem_sets_id: str):
        uri = f'/api/problem-sets/{problem_sets_id}/exam-problem-status'
        return ProblemStatus(self._get(uri))

    def problem_sets_exam_list(self, problem_sets_id: str, exam_id: str, problem_type, page: int, limit: int):
        uri = f'/api/problem-sets/{problem_sets_id}/exam-problem-list?exam_id={exam_id}&problem_type={problem_type}&page={page}&limit={limit}'
        return ProblemExamList(self._get(uri))

    def problem_sets_exam(self, problem_sets_id: str, exam_problem_id: str, problem_type):
        uri = f'/api/problem-sets/{problem_sets_id}/exam-problems/?exam_id={exam_problem_id}&problem_type={problem_type}'
        return ProblemExam(self._get(uri))

    def problem_sets_exam_problem(self, problem_sets_id: str, exam_problem_id: str):
        uri = f'/api/problem-sets/{problem_sets_id}/exam-problems/{exam_problem_id}'
        return ProblemExamProblem(self._get(uri))

    def problem_sets_exam_problem_submission(self, problem_sets_id: str, exam_problem_id: str, problem_set_problem_id: str, compiler: str, program_content: str, problem_type: str):
        uri = f'/api/exams/{problem_sets_id}/submissions'
        return self._post(uri, json= {
            'details':[{
                'problemId': exam_problem_id,
                'problemSetProblemId': problem_set_problem_id,
                'programmingSubmissionDetail': {
                    'program': program_content,
                    'compiler': compiler.upper(),
                    }
                }],
            'problemType': problem_type,
            })

    def problem_sets_exam_problem_last_submissions(self, problem_sets_id: str, exam_problem_id: str):
        uri = f'/api/problem-sets/{problem_sets_id}/last-submissions?problem_set_problem_id={exam_problem_id}'
        return LastSubmissions(self._get(uri))



    def problem_sets_rankings(self, problem_sets_id: str, page: int, limit: int):
        uri = f'/api/problem-sets/{problem_sets_id}/rankings?page={page}&limit={limit}'
        return ProblemRanking(self._get(uri))

    def problem_types(self, problem_sets_id: str):
        uri = f'/api/problem-sets/{problem_sets_id}/problem-types'
        return ProblemTypes(self._get(uri))

