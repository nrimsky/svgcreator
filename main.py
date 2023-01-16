import openai
import cv2 as cv
import requests
from dotenv import load_dotenv
import os

load_dotenv()

POINT_DOWNSAMPLE = 8


def url_to_image(url, readFlag=cv.IMREAD_COLOR):
    img_data = requests.get(url).content
    with open("image.png", "wb") as handler:
        handler.write(img_data)
    return cv.imread("image.png", readFlag)


def gen_image(prompt):
    openai.api_key = os.getenv("OPEN_AI_KEY")
    response = openai.Image.create(prompt=prompt, n=1, size="256x256")
    image_url = response["data"][0]["url"]
    return image_url


def make_svg(img_url, exact, write, print_img_url):
    if print_img_url:
        print(img_url)
    img = url_to_image(img_url)
    blurred_img = cv.blur(img, ksize=(3, 3))
    edges = cv.Canny(blurred_img, 100, 200)
    contours, hierarchy = cv.findContours(edges, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    svg = ""
    svg += '<svg viewBox="0 0 256 256" xmlns="http://www.w3.org/2000/svg"> <path fill="none" stroke="black" d="'
    if exact:
        for line in contours:
            x, y = line[0][0]
            svg += f"M {x},{y} "
            for point in line[1:]:
                x, y = point[0]
                svg += f"L {x},{y} "
    else:
        for line in contours:
            for i in range(0, len(line) - POINT_DOWNSAMPLE, POINT_DOWNSAMPLE):
                x1, y1 = line[i][0]
                x2, y2 = line[i + POINT_DOWNSAMPLE // 3][0]
                x3, y3 = line[i + (2 * POINT_DOWNSAMPLE) // 3][0]
                x4, y4 = line[i + POINT_DOWNSAMPLE][0]
                svg += f"M {x1},{y1} C {x2},{y2} {x3},{y3} {x4},{y4} "

    svg += '"/></svg>'
    if write:
        with open("path.svg", "w") as svgfile:
            svgfile.write(svg)


def get_img(prompt, print_img_url=False, write=False, exact=False):
    url = gen_image(prompt)
    return make_svg(url, exact=exact, print_img_url=print_img_url, write=write)


def main():
    prompt = input("Prompt >> ").strip()
    prompt += ", on a white background, uncropped, white padding around"  # Works much better for edge detection
    get_img(prompt, print_img_url=True, write=True)


if __name__ == "__main__":
    main()
