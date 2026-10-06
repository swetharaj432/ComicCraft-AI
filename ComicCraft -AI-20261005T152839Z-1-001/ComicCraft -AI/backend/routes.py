import os
from pathlib import Path

from dotenv import load_dotenv

from fastapi import (
    APIRouter,
    Form,
    HTTPException,
    Request
)

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from gemini_service import generate_story

from pdf_service import create_pdf

from schemas import PromptRequest


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

PROJECT_DIR = BASE_DIR.parent

STATIC_DIR = PROJECT_DIR / "static"


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv(
    BASE_DIR / ".env",
    override=True
)


# ============================================================
# ROUTER
# ============================================================

router = APIRouter()


# ============================================================
# TEMPLATES
# ============================================================

templates = Jinja2Templates(
    directory=str(STATIC_DIR)
)


# ============================================================
# HOME
# ============================================================

@router.get(
    "/",
    response_class=HTMLResponse
)
async def home(
    request: Request
):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,
            "error": None
        }
    )


# ============================================================
# CREATE COMIC
# ============================================================

def create_comic(
    story_prompt: str,
    character_name: str,
    setting: str,
    tone: str,
    art_style: str
):

    # Generate story and visual ideas
    layout = generate_story(
        story_prompt=story_prompt,
        character_name=character_name,
        setting=setting,
        tone=tone,
        art_style=art_style
    )

    # Add fields required by PDF
    for panel in layout:

        panel["scene_description"] = (
            panel["scene"]
        )

        panel["caption"] = (
            panel["visual_idea"]
        )

        panel["narration"] = (
            f"Expression: "
            f"{panel['character_expression']}. "
            f"Background: "
            f"{panel['background']}. "
            f"Camera: "
            f"{panel['camera_angle']}."
        )

        # No image generation
        panel["image_url"] = ""

    # Create PDF
    pdf_url = create_pdf(
        layout
    )

    return layout, pdf_url


# ============================================================
# HTML GENERATION
# ============================================================

@router.post(
    "/generate",
    response_class=HTMLResponse
)
async def generate(
    request: Request,

    story_prompt: str = Form(...),

    character_name: str = Form(...),

    setting: str = Form(...),

    tone: str = Form(...),

    art_style: str = Form(...)
):

    try:

        layout, pdf_url = create_comic(
            story_prompt=story_prompt,
            character_name=character_name,
            setting=setting,
            tone=tone,
            art_style=art_style
        )

        return templates.TemplateResponse(
            request=request,
            name="comic_preview.html",
            context={
                "request": request,
                "layout": layout,
                "pdf_url": pdf_url
            }
        )

    except Exception as error:

        print("----------------------------------------")
        print("COMIC GENERATION ERROR")
        print("----------------------------------------")
        print(error)
        print("----------------------------------------")

        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "request": request,
                "error": str(error)
            },
            status_code=500
        )


# ============================================================
# JSON API
# ============================================================

@router.post(
    "/generate-comic/json"
)
async def generate_json(
    data: PromptRequest
):

    try:

        layout, pdf_url = create_comic(
            story_prompt=data.story_prompt,
            character_name=data.character_name,
            setting=data.setting,
            tone=data.tone,
            art_style=data.art_style
        )

        return {
            "success": True,
            "layout": layout,
            "pdf_url": pdf_url
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


# ============================================================
# HEALTH CHECK
# ============================================================

@router.get(
    "/health"
)
async def health():

    return {
        "status": "ok",
        "gemini_configured": bool(
            os.getenv("GEMINI_API_KEY")
        ),
        "model": os.getenv(
            "GEMINI_MODEL"
        ),
        "image_generation": False
    }