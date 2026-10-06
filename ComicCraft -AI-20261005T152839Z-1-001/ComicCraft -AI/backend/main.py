from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from routes import router


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

PROJECT_DIR = BASE_DIR.parent

STATIC_DIR = PROJECT_DIR / "static"

GENERATED_PANELS_DIR = BASE_DIR / "generated_panels"


# Create generated image directory
GENERATED_PANELS_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# FASTAPI APP
# ============================================================

app = FastAPI(
    title="ComicCraft",
    description="AI Comic Story Creator",
    version="1.0.0"
)


# ============================================================
# STATIC FILES
# ============================================================

app.mount(
    "/static",
    StaticFiles(
        directory=str(STATIC_DIR)
    ),
    name="static"
)


# ============================================================
# GENERATED PANEL IMAGES
# ============================================================

app.mount(
    "/generated_panels",
    StaticFiles(
        directory=str(GENERATED_PANELS_DIR)
    ),
    name="generated_panels"
)


# ============================================================
# ROUTES
# ============================================================

app.include_router(router)