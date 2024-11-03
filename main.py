import logging

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
import traceback
from prompts import prompt_template
from questions_answers import questions_answers, save_questions_answers

logger = logging.getLogger(__name__)

app = FastAPI()

openai.api_key = ""
class Query(BaseModel):
    question: str
    user: str

@app.post("/ask")
async def ask_question(query: Query):
    try:
        print("query: "+ query.question)
        print("user: "+ query.user)
        print("came inside the controller")
        with open("explanations.txt", "r") as file:
            existing_explanation = file.read()
        prompt = prompt_template.format(question=query.question, user=query.user ,encoded_explanation=existing_explanation)
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500
        )

        answer = response.choices[0].message.content
        questions_answers.append({"question": query.question, "answer": answer})
        save_questions_answers()
        return {"question": query.question, "answer": answer}
    except Exception as e:
        stack_trace = traceback.format_exc()
        print("stack trace"+ str(e))
        print(stack_trace)
        raise HTTPException(status_code=500, detail=str(e))