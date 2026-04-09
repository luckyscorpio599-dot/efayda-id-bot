import os
import base64

# 1. Get the current directory
base_dir = os.path.dirname(os.path.abspath(__file__))
# 2. Join it with the filename
TEMPLATE_PATH = os.path.join(base_dir, "template.png")

# 3. Open and read the file (Notice the spaces below!)
with open(TEMPLATE_PATH, "rb") as f:
    template_data = f.read()  # This line MUST have 4 spaces before it
    TEMPLATE_BASE64 = base64.b64encode(template_data).decode('utf-8') # This one too
