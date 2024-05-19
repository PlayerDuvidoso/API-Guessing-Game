from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pydantic import BaseModel
from dotenv import dotenv_values
from typing import Optional

# --> Configuration <--
config = dotenv_values(".env")


# --> MongoDB (Connection/Database/Collection) <--
db_con = MongoClient(config.get('uri'), server_api=ServerApi('1'))
db = db_con.get_database('AGG-DB')
questions = db.get_collection('Questions')


# --> Data Models <--
class QuestionDisplay(BaseModel):
    id: int
    display: str

class Question(BaseModel):
    id: Optional[int] = None
    question_type: str
    result: int
    display: str


# --> Methods <--
def check_id(id: int) -> dict:

    if questions.count_documents({}) > 0:
        question = questions.find_one({'id': id})
        return question if question else False
    return False


def get_id():
    if questions.count_documents({}) > 0:
        id = questions.find_one(sort=[('id', -1)])['id'] + 1
        print(f'{id} <- Question ID')
        return int(id)
    return 1
             

def add_question(question: dict):
    if not check_id(question['id']):
        questions.insert_one(question)
        print(f'Question ID:{question.get("id")} added to database!')
        return QuestionDisplay(id=question.get('id'), display=question.get('display'))


def get_question(id: int):
    question = questions.find({'id': id})
    if not question:
        raise Exception('ID not found!')
    return question
        
    
    