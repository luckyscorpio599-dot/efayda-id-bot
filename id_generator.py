import os
from PIL import Image, ImageDraw, ImageFont
from template_base64 import TEMPLATE_PATH

# Get the current directory of this script
base_dir = os.path.dirname(os.path.abspath(__file__))

# Point to the font.ttf file you uploaded to GitHub
FONT_PATH = os.path.join(base_dir, "font.ttf")

# Load fonts with a fallback in case the file is missing
try:
    font_large = ImageFont.truetype(FONT_PATH, 36)
    font_medium = ImageFont.truetype(FONT_PATH, 28)
except OSError:
    print("Warning: font.ttf not found, using default font.")
    font_large = ImageFont.load_default()
    font_medium = ImageFont.load_default()

def generate_id_image(data, photo, qr, barcode):
    template = Image.open(TEMPLATE_PATH).convert("RGBA")
    draw = ImageDraw.Draw(template)

    # TEXT positions — adjust to your template
    draw.text((330, 280), data["full_name_en"], font=font_large, fill="black")
    draw.text((330, 350), data["dob"], font=font_medium, fill="black")
    draw.text((330, 420), data["sex"], font=font_medium, fill="black")
    draw.text((330, 500), data["fan"], font=font_medium, fill="black")
    draw.text((330, 570), data["fin"], font=font_medium, fill="black")
    draw.text((200, 650), data["phone"], font=font_medium, fill="black")
    draw.text((200, 680), data["region"], font=font_medium, fill="black")
    draw.text((200, 710), data["zone"], font=font_medium, fill="black")
    draw.text((200, 740), data["woreda"], font=font_medium, fill="black")
    draw.text((850, 680), data["serial"], font=font_medium, fill="black")

    # IMAGE placement
    template.paste(photo, (100, 250))
    template.paste(qr, (900, 350))
    template.paste(barcode, (300, 750))

    output = "final_id.png"
    template.save(output)
    return output
