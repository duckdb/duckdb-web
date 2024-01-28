import json
from pathlib import Path
from argparse import ArgumentParser
from subprocess import check_output, CalledProcessError, PIPE
import re

with open("docs/functions.json", "r") as functions_json_content:
    functions = json.load(functions_json_content)

categories = {f["category"] for f in functions}
categories = sorted(categories)

print(categories)

with open("out.md", "w") as out:
    for category in categories:
        category_functions = [f for f in functions if f["category"] == category]

        out.write(f"## {category.capitalize()} Functions\n\n")
        out.write(f"| Name | Description |\n")
        out.write(f"|---|------------|\n")
        for f in category_functions:
            f["parameter_list"] = "`, `".join(
                [f"*`{param}`*" for param in f["parameters"]]
            )
            f["signature_md"] = f"""`{f["name"]}(`{f["parameter_list"]}`)`"""
            f["anchor"] = re.sub(r"[^a-zA-Z_]", "", f["signature_md"])

            out.write(
                f"""| [{f["signature_md"]}](#{f["anchor"]}) | {f["description"]} | \n"""
            )
        out.write("\n")

        for f in category_functions:
            out.write(f"""### {f["signature_md"]}\n\n""")
            out.write(f"""* **Description:** {f["description"]}\n""")
            out.write(f"""* **Example:** `{f["example"]}`\n""")
            out.write(f"""* **Result:** `{f["result"]}`\n""")
            out.write(f"\n")
