from PIL import Image, ImageDraw, ImageFont
import numpy as np

def crop_and_resize(img:Image.Image, output_size=(480,800)):
    target_width, target_height = output_size
    
    # Calculate aspect ratios
    img_ratio = img.width / img.height
    target_ratio = target_width / target_height
    
    # Determine crop dimensions
    if img_ratio > target_ratio:
        # Image is wider than target - crop sides
        new_height = img.height
        new_width = int(img.height * target_ratio)
        left = (img.width - new_width) / 2
        top = 0
    else:
        # Image is taller than target - crop top/bottom
        new_width = img.width
        new_height = int(img.width / target_ratio)
        left = 0
        top = (img.height - new_height) / 2
    
    # Crop and resize
    img = img.crop((left, top, left + new_width, top + new_height))
    img = img.resize(output_size)
    
    return img


def get_bottom_dominant_color(image, region_height=10):
    img_array = np.array(image)
    bottom_region = img_array[-region_height:, :, :]
    avg_color = np.mean(bottom_region, axis=(0, 1)).astype(int)
    return tuple(avg_color)


def is_white_visible(rgb, threshold=128):
    """Simple brightness check (0-255)"""
    r, g, b = rgb
    brightness = (r * 299 + g * 587 + b * 114) / 1000
    return brightness < threshold  # Darker colors show white well


def add_title_in_rounded_rectangle(img:Image.Image, text:str, rect_height=40, border_width=3)->Image.Image:
    width, height = img.size
    margin=20
    margin_bottom = 10
    dominant_color = get_bottom_dominant_color(img, rect_height+margin_bottom)
    
    draw = ImageDraw.Draw(img)

    font = ImageFont.truetype("font/SpecialElite.ttf", 22, encoding="unic")
    # Get text bounding box (left, top, right, bottom)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]  # right - left
    text_height = bbox[3] - bbox[1]  # bottom - top
    
    txt_x = (img.width - text_width) / 2
    txt_y = (height -margin_bottom  -text_height/2 -rect_height/2) 

    draw_color = "white" if is_white_visible(dominant_color) else "black"
    
    draw.rounded_rectangle( (margin, height -margin_bottom -rect_height, width-margin, height -margin_bottom), 
                           radius=20, fill=dominant_color, outline=draw_color, width=border_width)
    
    draw.text(( txt_x, txt_y), text, fill=draw_color, font=font )
    
    return img


def process_image(img:Image.Image, title="")->Image.Image:
    img = crop_and_resize(img).convert('RGB')
    
    if title != "":
        img = add_title_in_rounded_rectangle(img,title)
    
    img = img.rotate(-90, expand=True) 
    
    return img
