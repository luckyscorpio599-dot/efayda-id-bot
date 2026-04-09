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

    # --- 1. RESIZE IMAGES TO FIT BOXES ---
    # Adjust these sizes if they look too small/large on your phone
    photo = photo.resize((240, 300))      # Height/Width for the portrait
    qr = qr.resize((160, 160))           # Square for QR
    barcode = barcode.resize((380, 70))  # Long/Thin for Barcode

    # --- 2. TEXT POSITIONS (Adjusted for your template) ---
    # We increased the Y (second number) to move text down
    draw.text((330, 310), data["full_name_en"], font=font_large, fill="black")
    draw.text((330, 380), data["dob"], font=font_medium, fill="black")
    draw.text((330, 450), data["sex"], font=font_medium, fill="black")
    draw.text((330, 520), data["fan"], font=font_medium, fill="black")
    draw.text((330, 590), data["fin"], font=font_medium, fill="black")
    
    # Address section
    draw.text((200, 680), data["phone"], font=font_medium, fill="black")
    draw.text((200, 710), data["region"], font=font_medium, fill="black")
    draw.text((200, 740), data["zone"], font=font_medium, fill="black")
    draw.text((200, 770), data["woreda"], font=font_medium, fill="black")
    draw.text((850, 710), data["serial"], font=font_medium, fill="black")

    # --- 3. IMAGE PLACEMENT ---
    # Moved Y coordinates down to prevent overlapping the header
    template.paste(photo, (70, 300))     # Moved photo down and left
    template.paste(qr, (880, 380))       # Moved QR to the right side
    template.paste(barcode, (350, 830))  # Moved barcode to bottom center

    output = "final_id.png"
    template.save(output)
    return output
