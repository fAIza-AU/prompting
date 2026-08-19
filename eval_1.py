from bb import ask_llm
from judge import groq_llm
import json 
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
my_key = os.environ.get('SECRET_KEY')

client = Groq(api_key=my_key)
with open("test_cases.json") as f:
    all_cases = json.load(f)

def eval_llm (article,limit):
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {'role': 'system', 'content': f"You are a professional writer. Summarize the article without exceeding {limit} words. Do not use bullet points or headers, do not exceed it in any circumstances, even if it mean dropping unneccessary words that wont break the summary."},
            {'role': 'user', 'content': article}
        ]
    )
    return response.choices[0].message.content
  

for case in all_cases:
    print(case['id'])
    article = case['source_text']
    limit = case['must_not_exceed_words']
    summary = eval_llm(article, limit)
    summary = summary.replace("\u202f", " ")
    words = summary.split()
    length = len(words)
   
    if length > limit:
        print("FAIL - too long")
    else:
        print("PASS")
    for text in case['must_include']:
        if text in summary:
            print('found:', text)
        else:
            print('MISSING:', text)
    Question = groq_llm(summary, case['must_include'])
    print('JUDGE SAYS:', Question)
    print(summary)
    print('*********************')

