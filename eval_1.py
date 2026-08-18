from bb import ask_llm
from judge import groq_llm
import json 
with open("test_cases.json") as f:
    all_cases = json.load(f)

for case in all_cases:
    print(case['id'])
    article = case['source_text']
    
    summary = ask_llm(article)
    summary = summary.replace("\u202f", " ")
    words = summary.split()
    length = len(words)
    limit = case['must_not_exceed_words']
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
  



