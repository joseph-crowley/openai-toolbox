from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.urls import reverse
from django.contrib import messages
from django.conf import settings
from django.templatetags.static import static
from openai_toolbox.dalle import generate_image

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
        if user_input == 'clear':
            with open(f'conversations/basic.json', 'r') as infile:
                conversation = json.load(infile)
                request.session['messages'] = conversation
                return render(request, 'chat/conversation.html', {'messages': conversation})
        openai.api_key = os.environ.get("OPENAI_API_KEY")

        # Get previous conversation
        conversation = request.session.get('messages', [])

        # add the new message
        if user_input:
            conversation.append({"role": "user", "content": user_input})

        # Get optional parameters from the request
        temperature = float(request.POST.get('temperature', 1))
        top_p = float(request.POST.get('top_p', 1))
        n = int(request.POST.get('n', 1))
        stream = request.POST.get('stream', 'false').lower() == 'true'
        stop = request.POST.get('stop', None)
        max_tokens = int(request.POST.get('max_tokens', 0)) or None
        presence_penalty = float(request.POST.get('presence_penalty', 0))
        frequency_penalty = float(request.POST.get('frequency_penalty', 0))
        logit_bias = json.loads(request.POST.get('logit_bias', "{}"))
        user_id = request.POST.get('user', '')

        # generate text
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation,
            temperature=temperature,
            top_p=top_p,
            n=n,
            stream=stream,
            stop=stop,
            max_tokens=max_tokens,
            presence_penalty=presence_penalty,
            frequency_penalty=frequency_penalty,
            logit_bias=logit_bias,
            user=user_id,
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
        with open(f'saved_conversations/{file_name}', 'w') as outfile:
            json.dump(conversation, outfile, indent=4)

        messages.success(request, f"Conversation saved as {file_name}.")
        return redirect('chat')
    else:
        return redirect('chat')

def select_conversation(request):
    if request.method == 'POST':
        conversation_file = request.POST['conversation_file']

        # if the file has a date in the name, load it from saved_conversations
        if '2023' in conversation_file:
            conversation_dir = 'saved_conversations'
        else:
            conversation_dir = 'conversations'

        try:
            with open(f'{conversation_dir}/{conversation_file}', 'r') as infile:
                conversation = json.load(infile)
                request.session['messages'] = conversation
                return render(request, 'chat/conversation.html', {'messages': conversation})
        except FileNotFoundError:
            conversation_files = os.listdir('conversations')
            saved_files = os.listdir('saved_conversations')
            return render(request, 'chat/select_conversation.html', {'error_message': 'File not found. Please try again.', 'conversation_files': conversation_files, 'saved_conversations': saved_files})

    else:
        conversation_files = os.listdir('conversations')
        saved_files = os.listdir('saved_conversations')
        return render(request, 'chat/select_conversation.html', {'conversation_files': conversation_files, 'saved_conversations': saved_files})

def dalle(request):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        prompt = request.GET.get("prompt", "")
        if not prompt:
            return JsonResponse({"error": "Prompt is required."}, status=400, content_type="application/json")

        try:
            image_path = generate_image(prompt)
            return JsonResponse({"image_path": image_path}, content_type="application/json")
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500, content_type="application/json")
    else:
        return render(request, 'chat/dalle.html')


def image_gallery(request):
    image_folder = os.path.join(settings.BASE_DIR, 'static','assets','generated_images')
    image_files = [f for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f))]
    image_urls = [static(f"assets/generated_images/{img}") for img in image_files]

    context = {
        'image_data': zip(image_urls, image_files)
    }

    return render(request, 'chat/image_gallery.html', context)
