from django.shortcuts import render
from django.http import JsonResponse
from django.urls import reverse
import json
import os
import openai

def home(request):
    context = {
        'chat_url': 'chat',
        'panel_images': [
            {'img': 'static/assets/images/home/img1.jpg', 'url': '/chat'},
            {'img': 'static/assets/images/home/img2.jpg', 'url': '/chat'},
            {'img': 'static/assets/images/home/img3.jpg', 'url': '/chat'},
        ]
    }

    return render(request, 'home.html', context)

def submit_message(request):
    if request.method == 'POST':
        user_input = request.POST['message']
        openai.api_key = os.environ.get("OPENAI_API_KEY")

        # Get previous conversation
        conversation = request.session.get('conversation', [])

        # Convert conversation to messages format
        messages = [{"role": "system", "content": "You are an AI trained to help users with their questions."}]
        for message in conversation:
            messages.append({"role": "user", "content": message["user_input"]})
            messages.append({"role": "assistant", "content": message["bot_response"]})
        messages.append({"role": "user", "content": user_input})

        # generate text
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        bot_response = response.choices[0].message["content"]
        conversation.append({"user_input": user_input, "bot_response": bot_response})
        request.session['conversation'] = conversation
        return render(request, 'chat/conversation.html', {'conversation': conversation})
    else:
        conversation = request.session.get('conversation', [])
        return render(request, 'chat/conversation.html', {'conversation': conversation})

