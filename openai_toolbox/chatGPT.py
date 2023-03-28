import openai
import os
from django.conf import settings

openai.api_key = settings.OPENAI_API_KEY

def generate_message(conversation, **kwargs):
    fail_ctr = 0
    while True:
        try:
            response = openai.ChatCompletion.create(
                    model=settings.GPT_MODEL,
                    messages=conversation,
                    **kwargs
               )
            return response.choices[0].message["content"]
        except Exception as err:
            print(f'Error: {err}')
            os.system(f'sleep {fail_ctr * 5}')
            fail_ctr += 1
            if fail_ctr > 5:
                raise err
            continue

