import openai
import os
import json
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.environ.get("OPENAI_API_KEY")

def generate_docstring(code):
    """
    Generates a docstring for the given file using OpenAI's Chat Completion.

    Args:
        code (str): Contents the file ('js', 'py', 'css', or 'html').

    Returns:
        str: The generated docstring.
    """

    # Create a prompt for the model
    system_prompt = f"Write a comprehensive docstring for the code provided, which will serve as a guide for developers. Include the following information in the docstring:\n1. The main purpose and functionality of the code\n2. Related files and dependencies\n3. Location of key implementation details\n4. Any additional information essential for understanding and maintaining the code."
    user_prompt = f"Here is the code:\n```\n{code}\n```\n"

    # Set model parameters
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
                ],
            temperature=0.8,
            max_tokens=500,
        )

        # Extract the generated docstring
        docstring = response.choices[0].message["content"].strip()
    except Exception as err:
        print(err.args[0])
        return f'FAILED TO GENERATE DOCSTRING\n\n{err.args[0]}'

    return docstring

def extract_files(path):
    relevant_files = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(('.js', '.py', '.html', '.css')):
                relevant_files.append(os.path.join(root, file))
    return relevant_files

def encode_files(files):
    encoded_messages = []

    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
        message = {
        "role": "user",
        "content": f'FILE: {file}\n\nCODE:\n```\n{content}\n```',
        "file": file,
        "author": "Joe Crowley",
        "year": "2023",
        "docs": generate_docstring(content)
        }
        encoded_messages.append(message)

        print(f'docs for {file}:\n{message["docs"]}\n\n')

    return encoded_messages

def save_as_json(data, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def add_docstrings_to_files(docs_list):
    def get_comment_syntax(file_type):
        if file_type == 'py':
            return '"""', '"""'
        elif file_type == 'C' or file_type == 'cpp' or file_type == 'cxx' or file_type == 'cc':
            return '/*', '*/'
        elif file_type == 'js' or file_type == 'css':
            return '/*', '*/'
        elif file_type == 'html':
            return '<!--', '-->'
        else:
            raise ValueError(f"Unsupported file type: {file_type}")

    for doc in docs_list:
        file_path = doc["file"]
        file_type = file_path.split('.')[-1]
        docs = doc["docs"]
        year = doc["year"]
        author = doc["author"]

        start_comment, end_comment = get_comment_syntax(file_type)

        with open(file_path, 'r') as file:
            file_content = file.read()

        modified_content = f"{start_comment}\n{docs}\n\nCopyright {year}, {author}, All rights reserved.\n{end_comment}\n{file_content}"

        with open(f'{file_path}.update', 'w') as file:
            file.write(modified_content)

if __name__ == '__main__':
    project_directory = '.' # Set to the root directory of your Django project
    relevant_files = extract_files(project_directory)
    encoded_messages = encode_files(relevant_files)
    output_file = 'docs.json'
    save_as_json(encoded_messages, output_file)
    with open(output_file,'r') as f:
        docs_list = json.load(f)
    add_docstrings_to_files(docs_list)
