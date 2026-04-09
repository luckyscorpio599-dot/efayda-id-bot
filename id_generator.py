import os
from PIL import Image, ImageDraw, ImageFont
from template_base64 import TEMPLATE_PATH

base_dir = os.path.dirname(os.path.abspath(__file__))
FONT_PATH = os.path.join(base_dir, "font.ttf")

try:
    # Font sizes adjusted for the template resolution
    font_large = ImageFont.truetype(FONT_PATH, 38)
    font_medium = ImageFont.truetype(FONT_PATH, 28)
    font_small = ImageFont.truetype(FONT_PATH, 22)
except OSError:
    font_large = ImageFont.load_default()
    font_medium = ImageFont.load_default()
    font_small = ImageFont.load_default()

def generate_id_image(data, photo, qr, barcode):
    # Open template and ensure it's in RGBA mode
    template = Image.open(TEMPLATE_PATH).convert("RGBA")
    draw = ImageDraw.Draw(template)

    # 1. RESIZE ASSETS
    # Main ID Photo
    photo_main = photo.resize((210, 260))
    # Small Photo for the bottom security area
    photo_tiny = photo.resize((75, 95))
    # QR Code
    qr_code = qr.resize((240, 240))
    # Barcode
    barcode_img = barcode.resize((320, 65))

    # 2. PLACE IMAGES (Based on your blank template)
    template.paste(photo_main, (45, 285))      # Primary Portrait
    template.paste(qr_code, (740, 80))         # Upper Right QR
    template.paste(barcode_img, (230, 755))    # Bottom Barcode
    template.paste(photo_tiny, (390, 645))     # Small Ghost Portrait

    # 3. DRAW TEXT (Front/Left Side)
    # Full Name
    draw.text((205, 335), data.get("full_name_en", ""), font=font_large, fill="black")
    # Date of Birth
    draw.text((205, 435), data.get("dob", ""), font=font_medium, fill="black")
    # Sex
    draw.text((205, 530), data.get("sex", ""), font=font_medium, fill="black")
    # FAN (The ID Number)
    draw.text((260, 725), data.get("fan", ""), font=font_medium, fill="#8B6914") # Golden-brown color

    # 4. DRAW TEXT (Back/Right Side)
    # Region/Address info
    draw.text((570, 110), data.get("phone", ""), font=font_medium, fill="black")
    draw.text((570, 210), data.get("region", ""), font=font_medium, fill="black")
    draw.text((570, 315), data.get("zone", ""), font=font_medium, fill="black")
    draw.text((570, 425), data.get("woreda", ""), font=font_medium, fill="black")
    
    # FIN and Serial
    draw.text((630, 725), data.get("fin", ""), font=font_medium, fill="black")
    draw.text((930, 825), data.get("serial", "1000"), font=font_small, fill="black")

    output = "final_id.png"
    template.save(output)
    return output
