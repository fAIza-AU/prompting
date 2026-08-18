import os
from dotenv import load_dotenv
load_dotenv()
from groq import Groq 
my_key = os.environ.get('SECRET_KEY')


client = Groq(api_key=my_key)



def groq_llm(summary,must_include):
    user_question=f"Does this summary: {summary} correctly mention these texts:{must_include}? Answer only YES OR NO."
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {'role': 'system', 'content': 'You are a strict grader. Answer only YES or NO.'},
            {'role': 'user', 'content': user_question}
        ]
    )
    return response.choices[0].message.content 

