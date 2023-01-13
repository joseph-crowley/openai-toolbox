from django.shortcuts import render
from django.http import JsonResponse
import json
import openai

def submit_message(request):
    if request.method == 'POST':
        user_input = request.POST['message']
        openai.api_key = "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"

        # generate text
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=user_input,
            max_tokens=3600,
            n = 1,
            stop=None,
            temperature=0.5,
        )
        bot_response = ''.join(response["choices"][0]["text"])
        conversation = request.session.get('conversation', [])
        conversation.append({"user_input": user_input, "bot_response": bot_response})
        request.session['conversation'] = conversation
        return render(request, 'chat/conversation.html', {'conversation': conversation})
    else:
        conversation = request.session.get('conversation', [])
        return render(request, 'chat/conversation.html', {'conversation': conversation})


