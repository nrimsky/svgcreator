import openai
import cv2 as cv
import requests
from dotenv import load_dotenv
import os
import numpy as np
from scipy.interpolate import splprep, splev

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


def make_svg(img_url):
    print(f"Processing image {img_url}")
    img = url_to_image(img_url)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    blurred_img = cv.GaussianBlur(gray, (5, 5), 0)
    thresh = cv.adaptiveThreshold(blurred_img, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 11, 2)
    contours, _ = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    
    svg = '<svg viewBox="0 0 256 256" xmlns="http://www.w3.org/2000/svg">'
    seen = set()
    for contour in contours:
        # Use Douglas-Peucker algorithm to reduce points
        epsilon = 0.4
        approx = cv.approxPolyDP(contour,epsilon,True)

        # Ensure that approx is iterable
        if len(approx) < 2:
            continue

        # Compute hash of contour and check if it's similar to a seen one
        contour_hash = hash(tuple(map(tuple, np.squeeze(approx))))
        if contour_hash in seen:
            continue
        seen.add(contour_hash)

        # Compute average color and use as stroke color
        mask = np.zeros(img.shape[:2], np.uint8)
        cv.drawContours(mask, [approx], -1, (255), thickness=cv.FILLED)
        mean_val = cv.mean(img, mask=mask)
        stroke_color = '#%02x%02x%02x' % (int(mean_val[2]), int(mean_val[1]), int(mean_val[0]))  # BGR to hex

        # Generate SVG path
        svg += f'<path fill="none" stroke="{stroke_color}" d="'
        x, y = approx[0][0]
        svg += f"M {x},{y} "
        for point in approx[1:]:
            x, y = point[0]
            svg += f"L {x},{y} "
        svg += '"/>\n'

    svg += '</svg>'
    with open("path.svg", "w") as svgfile:
        svgfile.write(svg)



def get_img(prompt):
    # url = gen_image(prompt)
    url = "https://oaidalleapiprodscus.blob.core.windows.net/private/org-OM6lB4JDo340cfkoFmYsZUYH/user-u8jcWO9LXLQReA4OZqot4gIf/img-JBhutqAmGj8BFHEpVZFQAlvj.png?st=2023-06-28T16%3A27%3A02Z&se=2023-06-28T18%3A27%3A02Z&sp=r&sv=2021-08-06&sr=b&rscd=inline&rsct=image/png&skoid=6aaadede-4fb3-4698-a8f6-684d7786b067&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2023-06-28T00%3A07%3A09Z&ske=2023-06-29T00%3A07%3A09Z&sks=b&skv=2021-08-06&sig=mcEfATCKn0yzU1TxC8WHSHbWtaOPdO405HiEcrfkMvY%3D"
    return make_svg(url)


def main():
    prompt = input("Prompt >> ").strip()
    prompt += " - Ensure subjects are centered, surrounded by ample white padding. Use a cartoon logo style with a strong, clear outline and vibrant color fill."
    get_img(prompt)


if __name__ == "__main__":
    main()
