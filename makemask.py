from PIL import Image, ImageDraw

# Define the dimensions of the mask
mask_size = (256, 256)
center_size = (200, 200)

# Create a new white image with the mask size
white_mask = Image.new('RGB', mask_size, (255, 255, 255))

# Save the white mask image
white_mask.save('white_mask.png')

# Create a new transparent image with the mask size
transparent_mask = Image.new('RGBA', mask_size, (255, 255, 255, 0))

# Calculate the position of the center
center_position = ((mask_size[0] - center_size[0]) // 2, (mask_size[1] - center_size[1]) // 2)

# Create a white rectangle for the entire mask
mask_draw = ImageDraw.Draw(transparent_mask)
mask_draw.rectangle([(0, 0), mask_size], fill=(255, 255, 255, 255))

# Create a transparent rectangle for the center
mask_draw.rectangle([(center_position[0], center_position[1]), (center_position[0] + center_size[0], center_position[1] + center_size[1])], fill=(255, 255, 255, 0))

# Save the transparent mask image
transparent_mask.save('transparent_mask.png')
