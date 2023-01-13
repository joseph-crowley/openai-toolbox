# openai-toolbox

This is a simple Django app that serves a home page with photos and a chat endpoint that uses the OpenAI API to call the Davinci-003 model.
Installation

### Clone the repository and navigate to the project directory.

    git clone https://github.com/joseph-crowley/openai-toolbox.git
    cd django-photo-chat-app

### Create a new conda environment and activate it.

    conda create --name gpt --file conda.env
    conda activate gpt

### Copy the .env.example file to a new file called .env and add your OpenAI API key.

    cp .env.example .env
    
    # add your key
    vim .env 

### Run migrations and start the development server.

    python manage.py makemigrations
    python manage.py migrate
    python manage.py runserver

## Usage

    Visit http://localhost:8000 to view the home page with photos.
    Visit http://localhost:8000/chat to use the chat endpoint and interact with the Davinci-003 model.
