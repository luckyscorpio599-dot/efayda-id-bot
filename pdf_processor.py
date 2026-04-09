from PyPDF2 import PdfReader
from pdf2image import convert_from_path

def extract_pdf_data(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        t = page.extract_text()
        if t:
            text += t + "\n"

    def find_label(label):
        for line in text.split("\n"):
            if label in line:
                return line.replace(label, "").strip()
        return ""

    return {
        "full_name_am": find_label("ሙሉ ስም /"),
        "full_name_en": find_label("First, Middle, Surname"),
        "dob": find_label("የትውልድ ቀን /"),
        "sex": find_label("ፆታ /"),
        "nationality": find_label("ዜግነት /"),
        "phone": find_label("ስልክ /"),
        "region": find_label("ክልል /"),
        "zone": find_label("ክፍለ ከተማ / ዞን"),
        "woreda": find_label("ወረዳ /"),
        "fan": find_label("FCN:"),
        "fin": find_label("FIN:"),
        "serial": find_label("Serial Number"),
        "date_issue": find_label("Date of Issue"),
        "date_expiry": find_label("Date of Expiry")
    }

def extract_images_from_pdf(pdf_path):
    pages = convert_from_path(pdf_path, dpi=300)
    img = pages[0]

    # Adjust coordinates to match your template
    photo = img.crop((100, 250, 330, 550))
    qr = img.crop((900, 350, 1100, 550))
    barcode = img.crop((300, 750, 900, 830))

    return photo, qr, barcode
