import json
import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env"


# ============================================================
# LOAD ENVIRONMENT
# ============================================================

load_dotenv(
    dotenv_path=ENV_FILE,
    override=True
)


# ============================================================
# GEMINI CONFIGURATION
# ============================================================

GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY"
)

GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.8-flash"
)


print("----------------------------------------")
print("ComicCraft Gemini Service")
print("----------------------------------------")
print("ENV FILE:", ENV_FILE)
print("API KEY LOADED:", bool(GEMINI_API_KEY))
print("MODEL:", GEMINI_MODEL)
print("IMAGE GENERATION: DISABLED")
print("----------------------------------------")


# ============================================================
# CLIENT
# ============================================================

def get_client():

    api_key = os.getenv(
        "GEMINI_API_KEY"
    )

    if not api_key:

        raise ValueError(
            "GEMINI_API_KEY is missing.\n"
            f"Expected .env file at:\n{ENV_FILE}"
        )

    return genai.Client(
        api_key=api_key
    )


# ============================================================
# CLEAN JSON
# ============================================================

def clean_json_response(text):

    if not text:

        raise ValueError(
            "Gemini returned an empty response."
        )

    text = text.strip()

    if text.startswith("```"):

        lines = text.splitlines()

        if lines:
            lines = lines[1:]

        if (
            lines
            and lines[-1].strip() == "```"
        ):
            lines = lines[:-1]

        text = "\n".join(lines).strip()

    return text


# ============================================================
# GENERATE COMIC STORY + VISUAL IDEAS
# ============================================================

def generate_story(
    story_prompt,
    character_name,
    setting,
    tone,
    art_style
):

    client = get_client()

    prompt = f"""
You are ComicCraft, an AI comic story creator.

Create a short 3-panel comic based on the user's idea.

USER STORY:
{story_prompt}

MAIN CHARACTER:
{character_name}

SETTING:
{setting}

TONE:
{tone}

ART STYLE:
{art_style}

IMPORTANT RULES:

1. Create exactly 3 panels.
2. Keep the same main character throughout all panels.
3. Make the story have a clear beginning, middle and ending.
4. Keep dialogue short and natural.
5. Do NOT generate images.
6. Instead, provide detailed visual ideas that an artist or
   image-generation tool could use later.
7. Keep the visual style consistent between panels.
8. Return ONLY valid JSON.
9. Do not use Markdown.
10. Do not use ```.

Each panel must contain:

- panel_number
- title
- scene
- dialogue
- visual_idea
- character_expression
- background
- camera_angle
- image_prompt

JSON format:

[
  {{
    "panel_number": 1,
    "title": "Beginning",
    "scene": "Short scene description",
    "dialogue": "Short dialogue",
    "visual_idea": "What the panel should look like",
    "character_expression": "Character facial expression",
    "background": "Background description",
    "camera_angle": "Camera/view description",
    "image_prompt": "Complete illustration idea"
  }},
  {{
    "panel_number": 2,
    "title": "Middle",
    "scene": "Short scene description",
    "dialogue": "Short dialogue",
    "visual_idea": "What the panel should look like",
    "character_expression": "Character facial expression",
    "background": "Background description",
    "camera_angle": "Camera/view description",
    "image_prompt": "Complete illustration idea"
  }},
  {{
    "panel_number": 3,
    "title": "Ending",
    "scene": "Short scene description",
    "dialogue": "Short dialogue",
    "visual_idea": "What the panel should look like",
    "character_expression": "Character facial expression",
    "background": "Background description",
    "camera_angle": "Camera/view description",
    "image_prompt": "Complete illustration idea"
  }}
]
"""

    try:

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )

    except Exception as error:

        print("----------------------------------------")
        print("GEMINI STORY GENERATION ERROR")
        print("----------------------------------------")
        print(error)
        print("----------------------------------------")

        raise

    if not response.text:

        raise ValueError(
            "Gemini returned an empty response."
        )

    text = clean_json_response(
        response.text
    )

    try:

        story = json.loads(
            text
        )

    except json.JSONDecodeError as error:

        print("----------------------------------------")
        print("INVALID GEMINI JSON")
        print("----------------------------------------")
        print(text)
        print("----------------------------------------")

        raise ValueError(
            "Gemini returned invalid JSON."
        ) from error

    # ========================================================
    # VALIDATE
    # ========================================================

    if not isinstance(
        story,
        list
    ):

        raise ValueError(
            "Gemini response must be a list."
        )

    if len(story) != 3:

        raise ValueError(
            f"Expected 3 panels, got {len(story)}."
        )

    required_fields = [
        "panel_number",
        "title",
        "scene",
        "dialogue",
        "visual_idea",
        "character_expression",
        "background",
        "camera_angle",
        "image_prompt"
    ]

    for index, panel in enumerate(
        story,
        start=1
    ):

        if not isinstance(
            panel,
            dict
        ):

            raise ValueError(
                f"Panel {index} is not a JSON object."
            )

        for field in required_fields:

            if field not in panel:

                raise ValueError(
                    f"Panel {index} is missing: {field}"
                )

    return story