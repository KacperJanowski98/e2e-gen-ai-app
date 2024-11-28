# pylint: disable=W0718

import base64
from typing import Any, Dict, List, Union


def format_content(content: Union[str, List[Dict[str, Any]]]) -> str:
    """Formats content as a string, handling both text and multimedia inputs."""
    if isinstance(content, str):
        return content
    if len(content) == 1 and content[0]["type"] == "text":
        return content[0]["text"]
    markdown = """Media:
"""
    text = ""
    for part in content:
        if part["type"] == "text":
            text = part["text"]
        # Local Images:
        if part["type"] == "image_url":
            image_url = part["image_url"]["url"]
            image_markdown = f'<img src="{image_url}" width="100">'
            markdown = (
                markdown
                + f"""
- {image_markdown}
"""
            )
        if part["type"] == "media":
            # Local other media
            if "data" in part:
                markdown = markdown + f"- Local media: {part['file_name']}\n"
    markdown = (
        markdown
        + f"""

{text}"""
    )
    return markdown

def get_parts_from_files(uploaded_files: List[Any]) -> List[Dict[str, Any]]:
    """Processes uploaded files and GCS URIs to create a list of content parts."""
    parts = []
    # read from local directly
    for uploaded_file in uploaded_files:
        im_bytes = uploaded_file.read()
        if "image" in uploaded_file.type:
            content = {
                "type": "image_url",
                "image_url": {
                    "url": f"data:{uploaded_file.type};base64,"
                    f"{base64.b64encode(im_bytes).decode('utf-8')}"
                },
                "file_name": uploaded_file.name,
            }
        else:
            content = {
                "type": "media",
                "data": base64.b64encode(im_bytes).decode("utf-8"),
                "file_name": uploaded_file.name,
                "mime_type": uploaded_file.type,
            }

        parts.append(content)
    return parts
