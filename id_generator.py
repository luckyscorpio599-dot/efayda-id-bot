import os
from PIL import Image, ImageDraw, ImageFont
from template_base64 import TEMPLATE_PATH

# Get the current directory of this script
base_dir = os.path.dirname(os.path.abspath(__file__))

# Point to the font.ttf file you uploaded to GitHub
FONT_PATH = os.path.join(base_dir, "font.ttf")

# Load fonts with a fallback in case the file is missing
try:
    font_large = ImageFont.truetype(FONT_PATH, 42) # Increased size for better visibility
    font_medium = ImageFont.truetype(FONT_PATH, 32) # Increased size
except OSError:
    print("Warning: font.ttf not found, using default font.")
    font_large = ImageFont.load_default()
    font_medium = ImageFont.load_default()

def generate_id_image(data, photo, qr, barcode):
    template = Image.open(TEMPLATE_PATH).convert("RGBA")
    draw = ImageDraw.Draw(template)

    # --- 1. RESIZE IMAGES (Aggressive resizing to ensure they fit) ---
    photo = photo.resize((260, 320))      
    qr = qr.resize((180, 180))           
    barcode = barcode.resize((400, 80))  

    # --- 2. TEXT POSITIONS (Significant shifts to force a change) ---
    # Moved everything significantly lower (Y values increased by 100+)
    draw.text((350, 420), data["full_name_en"], font=font_large, fill="black")
    draw.text((350, 490), data["dob"], font=font_medium, fill="black")
    draw.text((350, 560), data["sex"], font=font_medium, fill="black")
    draw.text((350, 630), data["fan"], font=font_medium, fill="black")
    draw.text((350, 700), data["fin"], font=font_medium, fill="black")
    
    # Address section - grouped lower down
    draw.text((220, 780), data["phone"], font=font_medium, fill="black")
    draw.text((220, 815), data["region"], font=font_medium, fill="black")
    draw.text((220, 850), data["zone"], font=font_medium, fill="black")
    draw.text((220, 885), data["woreda"], font=font_medium, fill="black")
    draw.text((860, 815), data["serial"], font=font_medium, fill="black")

    # --- 3. IMAGE PLACEMENT (New positions) ---
    template.paste(photo, (80, 420))     # Moved further down from the header
    template.paste(qr, (850, 450))       # Moved QR to the right center
    template.paste(barcode, (350, 920))  # Moved barcode to the very bottom

    output = "final_id.png"
    template.save(output)
    return output
