import openai
import requests
from django.conf import settings

openai.api_key = settings.OPENAI_API_KEY

def generate_image(prompt):
    # Call the DALL-E API
    response = openai.Image.create(
        prompt=prompt,
        n=1,  # Number of images to generate
        size="512x512",  # Image size
    )

    # Get the image URL from the response
    image_url = response['data'][0]['url']

    # Download the image
    response = requests.get(image_url)
    response.raise_for_status()

    # Save the image to the local system
    image_path = f"assets/generated_images/{prompt}.jpg"
    with open("static/"+image_path, "wb") as f:
        f.write(response.content)

    return image_path

