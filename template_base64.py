import os

# Get the current directory where the script is running
base_dir = os.path.dirname(os.path.abspath(__file__))
# Point to the template.png inside your project folder
template_image_path = os.path.join(base_dir, "template.png")

with open(template_image_path, "rb") as f:
    # ... your existing code to convert to base64 ...
