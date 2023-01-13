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
        user_input = request.POST.get('message')
        conversation_id = request.session.get('conversation_id')
        openai.api_key = os.environ.get("OPENAI_API_KEY")
        try:
            # generate text
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=user_input,
                #conversation_id = conversation_id,
                max_tokens=3600,
                n = 1,
                stop=None,
                temperature=0.5,
            )
            bot_response = response["choices"][0]["text"]
            print(bot_response)
            conversation = request.session.get('conversation', [])
            conversation.append({"user_input": user_input, "bot_response": bot_response})
            request.session['conversation'] = conversation
            return render(request, 'chat/conversation.html', {'conversation': conversation})
        except Exception as e:
            print(e.args[0])
            return render(request, 'chat/conversation.html', {'error': e.args[0]})
    else:
        conversation = request.session.get('conversation', [])
        return render(request, 'chat/conversation.html', {'conversation': conversation})


def select_conversation(request):
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    conversation_list = openai.Conversation.list()
    conversation_ids = [conversation.id for conversation in conversation_list["data"]]
    context = {'conversation_ids': conversation_ids}
    return render(request, 'chat/select_conversation.html', context)

def submit_conversation(request):
    if request.method == 'POST':
        conversation_id = request.POST['conversation_id']
        request.session['conversation_id'] = conversation_id
        return redirect('chat')


