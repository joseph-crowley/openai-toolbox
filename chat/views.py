from django.shortcuts import render
from django.http import JsonResponse
from django.urls import reverse
import json
import os
import openai
from logging_config import logger

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
        if not user_input:
            conversation = request.session.get('conversation', [])
            request.session['conversation'] = conversation
            return render(request, 'chat/conversation.html', {'conversation': conversation})
        openai.api_key = os.environ.get("OPENAI_API_KEY")
        try:
            # start streaming session
            session = openai.Completion.create(
                engine="text-davinci-003",
                prompt=user_input,
                max_tokens=3600,
                temperature=0.5,
                stop=None,
                stream=True
            )
            session_id = session["session_id"]
            request.session['session_id'] = session_id
            # generate text
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=user_input,
                session_id=session_id,
                max_tokens=3600,
                n = 1,
                stop=None,
                temperature=0.5,
            )
            logger.debug(dir(response))
            bot_response = " ".join([r["text"] for r in response])
            conversation = request.session.get('conversation', [])
            conversation.append({"user_input": user_input, "bot_response": bot_response})
            request.session['conversation'] = conversation
            return render(request, 'chat/conversation.html', {'conversation': conversation})
        except Exception as e:
            logger.debug(e.args[0])
            return render(request, 'chat/conversation.html', {'error': e.args[0]})
    else:
        conversation = request.session.get('conversation', [])
        return render(request, 'chat/conversation.html', {'conversation': conversation})



def select_conversation(request):
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    conversation_list = openai.Conversation.list()
    session_ids = [conversation.id for conversation in conversation_list["data"]]
    context = {'session_ids': session_ids}
    return render(request, 'chat/select_conversation.html', context)

def submit_conversation(request):
    if request.method == 'POST':
        session_id = request.POST['session_id']
        request.session['session_id'] = session_id
        return redirect('chat')


