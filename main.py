from fastapi import FastAPI
from pydantic import BaseModel
import random
import database as db


app = FastAPI()


# --> Response Models <--

class Answer(BaseModel):
    id: int
    result: int

class Summary(BaseModel):
    summary: str


# --> Methods <--

def create_question():
    types = ['sum', 'subtract', 'multiply', 'divide']
    numbers = sorted([random.randint(1, 1000), random.randint(1, 1000)], reverse=True)
    question_type = random.choice(types)

    match question_type:
        case 'sum':
            result = numbers[0]+numbers[1]
            display = f'{numbers[0]}+{numbers[1]}'
        case 'subtract':
            result = numbers[0]-numbers[1]
            display = f'{numbers[0]}-{numbers[1]}'
        case 'multiply':
            result = numbers[0]*numbers[1]
            display = f'{numbers[0]}*{numbers[1]}'
        case 'divide':
            result = int(numbers[0]/numbers[1])
            display = f'{numbers[0]}/{numbers[1]}'
    
    question = db.Question(id=db.get_id(), question_type=question_type, result=result, display=display)
    return db.add_question(question.model_dump())

# --> Endpoints <--

@app.get('/get_question')
async def get_question() -> db.QuestionDisplay:
    return create_question().model_dump_json()

@app.post('/post_answer')
async def post_question(answer: Answer) -> Summary:
    answer = answer.model_dump()
    question = db.check_id(answer.get('id'))
    if answer.get('result') == question.get('result'):
        return Summary(summary='Correct')
    else:
        return Summary(summary='Wrong!')