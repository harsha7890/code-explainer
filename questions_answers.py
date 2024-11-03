import json

questions_answers = []

def save_questions_answers():
    with open("questions_answers.json", "w") as f:
        json.dump(questions_answers, f, indent=4)