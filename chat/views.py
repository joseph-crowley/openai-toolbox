from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.urls import reverse
from django.contrib import messages

import json
import os
from datetime import datetime

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
        if user_input == 'clear': return render(request, 'chat/conversation.html', {'conversation': []})
        openai.api_key = os.environ.get("OPENAI_API_KEY")

        # Get previous conversation
        conversation = request.session.get('messages', [])

        # add the new message
        if user_input:
            conversation.append({"role": "user", "content": user_input})

        # generate text
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation
        )
        bot_response = response.choices[0].message["content"]
        conversation.append({"role": "assistant", "content": bot_response})
        request.session['messages'] = conversation

        # Save conversation to json file
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        with open(f'backup_conversations/conversation_{timestamp}.json', 'w') as outfile:
            json.dump(conversation, outfile, indent=4)

        return render(request, 'chat/conversation.html', {'messages': conversation})
    else:
        conversation = request.session.get('messages', [])
        return render(request, 'chat/conversation.html', {'messages': conversation})

def save_conversation(request):
    if request.method == 'POST':
        title = request.POST['title']
        conversation = request.session.get('messages', [])

        # Save conversation to a JSON file
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        file_name = f"{title}_{timestamp}.json"
        with open(f'backup_conversations/{file_name}', 'w') as outfile:
            json.dump(conversation, outfile, indent=4)

        messages.success(request, f"Conversation saved as {file_name}.")
        return redirect('submit_message')
    else:
        return redirect('submit_message')

def select_conversation(request):
    if request.method == 'POST':
        conversation_file = request.POST['conversation_file']

        try:
            with open(f'conversations/{conversation_file}', 'r') as infile:
                conversation = json.load(infile)
                request.session['messages'] = conversation
                return render(request, 'chat/conversation.html', {'messages': conversation})
        except FileNotFoundError:
            return render(request, 'chat/select_conversation.html', {'error_message': 'File not found. Please try again.'})

    else:
        conversation_files = os.listdir('conversations')
        return render(request, 'chat/select_conversation.html', {'conversation_files': conversation_files})

