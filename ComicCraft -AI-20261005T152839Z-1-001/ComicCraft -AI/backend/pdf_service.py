from datetime import datetime
from pathlib import Path

from fpdf import FPDF


BASE_DIR = Path(__file__).resolve().parent

EXPORT_DIR = (
    BASE_DIR
    / "static"
    / "exports"
)

EXPORT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


def _safe_text(value):

    return (
        str(value)
        .encode(
            "latin-1",
            "replace"
        )
        .decode("latin-1")
    )


def create_pdf(
    layout: list[dict]
) -> str:

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    filename = (
        f"comic_ideas_{timestamp}.pdf"
    )

    pdf_path = (
        EXPORT_DIR / filename
    )

    pdf = FPDF()

    pdf.set_auto_page_break(
        auto=True,
        margin=15
    )


    # ========================================================
    # TITLE PAGE
    # ========================================================

    pdf.add_page()

    pdf.set_font(
        "Helvetica",
        "B",
        24
    )

    pdf.cell(
        0,
        15,
        "ComicCraft",
        ln=True,
        align="C"
    )

    pdf.set_font(
        "Helvetica",
        "",
        12
    )

    pdf.multi_cell(
        0,
        8,
        _safe_text(
            "AI-generated comic story and "
            "illustration ideas"
        ),
        align="C"
    )

    pdf.ln(15)


    # ========================================================
    # PANELS
    # ========================================================

    for panel in layout:

        pdf.add_page()

        pdf.set_font(
            "Helvetica",
            "B",
            18
        )

        pdf.cell(
            0,
            12,
            _safe_text(
                f"Panel {panel['panel_number']}: "
                f"{panel['title']}"
            ),
            ln=True
        )

        pdf.ln(5)

        pdf.set_font(
            "Helvetica",
            "B",
            11
        )

        pdf.multi_cell(
            0,
            7,
            _safe_text(
                "Scene:"
            )
        )

        pdf.set_font(
            "Helvetica",
            "",
            11
        )

        pdf.multi_cell(
            0,
            7,
            _safe_text(
                panel["scene"]
            )
        )

        pdf.ln(4)

        pdf.set_font(
            "Helvetica",
            "B",
            11
        )

        pdf.multi_cell(
            0,
            7,
            "Dialogue:"
        )

        pdf.set_font(
            "Helvetica",
            "",
            11
        )

        pdf.multi_cell(
            0,
            7,
            _safe_text(
                panel["dialogue"]
            )
        )

        pdf.ln(4)

        pdf.set_font(
            "Helvetica",
            "B",
            11
        )

        pdf.multi_cell(
            0,
            7,
            "Visual Idea:"
        )

        pdf.set_font(
            "Helvetica",
            "",
            11
        )

        pdf.multi_cell(
            0,
            7,
            _safe_text(
                panel["visual_idea"]
            )
        )

        pdf.ln(4)

        pdf.set_font(
            "Helvetica",
            "B",
            11
        )

        pdf.multi_cell(
            0,
            7,
            "Character Expression:"
        )

        pdf.set_font(
            "Helvetica",
            "",
            11
        )

        pdf.multi_cell(
            0,
            7,
            _safe_text(
                panel["character_expression"]
            )
        )

        pdf.ln(4)

        pdf.set_font(
            "Helvetica",
            "B",
            11
        )

        pdf.multi_cell(
            0,
            7,
            "Background:"
        )

        pdf.set_font(
            "Helvetica",
            "",
            11
        )

        pdf.multi_cell(
            0,
            7,
            _safe_text(
                panel["background"]
            )
        )

        pdf.ln(4)

        pdf.set_font(
            "Helvetica",
            "B",
            11
        )

        pdf.multi_cell(
            0,
            7,
            "Camera Angle:"
        )

        pdf.set_font(
            "Helvetica",
            "",
            11
        )

        pdf.multi_cell(
            0,
            7,
            _safe_text(
                panel["camera_angle"]
            )
        )

        pdf.ln(4)

        pdf.set_font(
            "Helvetica",
            "B",
            11
        )

        pdf.multi_cell(
            0,
            7,
            "Image Generation Prompt:"
        )

        pdf.set_font(
            "Helvetica",
            "",
            11
        )

        pdf.multi_cell(
            0,
            7,
            _safe_text(
                panel["image_prompt"]
            )
        )


    # ========================================================
    # SAVE
    # ========================================================

    pdf.output(
        str(pdf_path)
    )

    return (
        f"/static/exports/{filename}"
    )