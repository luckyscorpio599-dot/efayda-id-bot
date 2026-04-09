import base64
import os

# Path to your template image
template_image_path = "/storage/emulated/0/Download/template.png"  # Adjust path if different

# Read the image and convert to Base64
with open(template_image_path, "rb") as f:
    data = f.read()
    encoded = base64.b64encode(data).decode("utf-8")

# Create the template_base64.py file
output_file = "/storage/emulated/0/Download/template_base64.py"  # Will save in Downloads
with open(output_file, "w") as f:
    f.write('TEMPLATE_BASE64 = """' + encoded + '"""\n')
    f.write('TEMPLATE_PATH = "template_combined.png"\n')
    f.write('import os, base64\n')
    f.write('if not os.path.exists(TEMPLATE_PATH):\n')
    f.write('    with open(TEMPLATE_PATH, "wb") as f:\n')
    f.write('        f.write(base64.b64decode(TEMPLATE_BASE64))\n')

print(f"template_base64.py created at {output_file}")