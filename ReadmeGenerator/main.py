"""
This script generates a README.md file and category-specific markdown files
for a GitHub profile based on a configuration file. It reads the configuration
from a JSON file, processes the data, and generates the markdown files.
"""

import json

try:
    from helpers import types, set_config
except ImportError:
    from .helpers import types, set_config

FILEPATH = "../"
FILENAME_BASE = "config_base.json"
FILENAME_PROJECTS = "config_projects.json"

f = open(FILENAME_BASE, "r", errors="ignore", encoding="utf-8")
data = json.loads(f.read())

readme_file = ""
context = {}

# for block in data:
#     if block["type"] == "config":
#         github_user = block["data"]["githubUser"]
#         categories = block["data"]["categories"]
#         context = set_config(github_user, categories)
#         continue

#     readme_file += types[block["type"]](block["data"], context)
#     readme_file += "\n\n"

# f = open(f"{FILEPATH}README.md", "w", errors="ignore", encoding="utf-8")
# f.write(readme_file)
# f.close()

# f = open(FILENAME_PROJECTS, "r", errors="ignore", encoding="utf-8")
# data = json.loads(f.read())

output = ""
right_image_block = None

# Primer bucle: para README.md
for block in data:
    if block["type"] == "config":
        github_user = block["data"]["githubUser"]
        categories = block["data"]["categories"]
        context = set_config(github_user, categories)
        continue
    if block["type"] == "rightImage":
        right_image_block = block
        continue
    if block["type"] == "intro":
        output += types[block["type"]](block["data"], context)
        # Insert rightImage immediately after intro
        if right_image_block:
            output += types["rightImage"](right_image_block["data"], context)
            right_image_block = None  # Solo insertar una vez
    else:
        output += types[block["type"]](block["data"], context)
    output += "\n\n"

with open(f"{FILEPATH}README.md", "w", errors="ignore", encoding="utf-8") as f:
    f.write(output)

# Segundo bucle: para archivos de categorías
for category in categories:
    current_file = ""
    temp_context = context.copy()
    temp_context["category"] = category["name"]
    temp_context["emoji"] = category["emoji"]
    temp_context["projects"] = [
        x for x in context["projects"] if category["tag"] in x["tags"]
    ]
    right_image_block = None
    for block in data:
        if block["type"] == "config":
            continue
        if block["type"] == "rightImage":
            right_image_block = block
            continue
        if block["type"] == "intro":
            current_file += types[block["type"]](block["data"], temp_context)
            # Insert rightImage immediately after intro
            if right_image_block:
                current_file += types["rightImage"](right_image_block["data"], temp_context)
                right_image_block = None
        else:
            current_file += types[block["type"]](block["data"], temp_context)
        current_file += "\n\n"

    with open(f"{FILEPATH}{category['tag']}.md", "w", errors="ignore", encoding="utf-8") as f:
        f.write(current_file)
