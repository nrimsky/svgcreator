import openai
import requests
from dotenv import load_dotenv
import os
from convert import png_to_svg

load_dotenv()

def url_to_image(url):
    img_data = requests.get(url).content
    with open("image.png", "wb") as handler:
        handler.write(img_data)
    return "image.png"


def gen_image(prompt):
    openai.api_key = os.getenv("OPEN_AI_KEY")
    response = openai.Image.create_edit(prompt=prompt, n=1, size="256x256", mask=open("transparent_mask.png", "rb"), image=open("white_mask.png", "rb"))
    image_url = response["data"][0]["url"]
    return image_url


def make_svg(img_url):
    print(f"Processing image {img_url}")
    img = url_to_image(img_url)
    png_to_svg(img, "path.svg")


def get_img(prompt):
    url = gen_image(prompt)
    return make_svg(url)


def main():
    prompt = input("Prompt >> ").strip()
    prompt += " (clear line drawing, colored, black outline, no text, clip art style, suitable for modern websites)"
    get_img(prompt)


if __name__ == "__main__":
    main()
