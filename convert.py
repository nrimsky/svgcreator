import cv2
import numpy as np
from skimage import measure
import svgwrite


def png_to_svg(input_path, output_path, threshold=128, smooth_factor=1.5):
    # Open the image file
    img = cv2.imread(input_path, 0)
    colored_img = cv2.imread(input_path)
    
    # Convert the image to binary
    _, img = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)

    # Find contours in the binary image
    contours = measure.find_contours(img, 0.8)

    # Initialize SVG canvas
    dwg = svgwrite.Drawing(output_path, profile='full')

    processed = set()

    # Iterate over all the contours and draw each one on the SVG canvas
    for contour in contours:
        # Correcting the format for OpenCV
        contour = contour.astype(np.int32)
        contour = np.expand_dims(contour, 1)

        # Smoothing contour and reducing keypoints
        contour = cv2.approxPolyDP(contour, smooth_factor, True)
        contour = contour[:, 0, :]  # Change back to original format
        
        # Avoiding duplicate lines
        line_string = ' '.join([f'{point[0]},{point[1]}' for point in contour])
        if line_string in processed:
            continue
        processed.add(line_string)

        points = [tuple(int(point) for point in contour_point) for contour_point in contour]

        # Flip the y-coordinates of the points
        points = [(y, x) for (x, y) in points]  # Swap x and y, and flip y-axis

        # Extracting color
        mask = np.zeros_like(img)
        cv2.drawContours(mask, [contour], -1, (255), thickness=cv2.FILLED)
        color = cv2.mean(colored_img, mask=mask)[:3]
        dwg.add(dwg.polygon(points=points, stroke='black', fill=svgwrite.utils.rgb(*color[::-1])))
    # Save the SVG
    dwg.save()