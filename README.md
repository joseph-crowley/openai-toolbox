# openai-toolbox

This is a simple Django app that serves a home page with photos and a chat endpoint that uses the OpenAI API to call a Chat Completions model.
Installation

### Clone the repository and navigate to the project directory.

    git clone https://github.com/joseph-crowley/openai-toolbox.git
    cd openai-toolbox

### Create a new conda environment and activate it.

    conda create --name gpt --file conda.env
    conda activate gpt

### Copy the .env.example file to a new file called .env and add your OpenAI API key.

    cp .env.example .env
    
    # add your key
    vim .env 

### Create directories for use in the app
    mkdir backup_conversations saved_conversations
    mkdir -p static/assets/generated_images

### Run migrations and start the development server.

    python manage.py makemigrations
    python manage.py migrate
    python manage.py runserver

## Usage

    Visit http://localhost:8000 to view the home page with photos.
    Visit http://localhost:8000/chat to use the chat endpoint and interact with the model.
    Visit http://localhost:8000/select_conversation to choose a preset.


    Type "clear" and hit "Submit" to clear the current conversation and start with a basic prompt
    Scroll down and provide a filename to save the conversation to saved_conversations/

