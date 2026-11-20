import os
from pathlib import Path
from typing import Union

from PIL import Image
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas


ImagePath = Union[str, os.PathLike]


def create(
    img: ImagePath,
    pageStart: int,
    pageStop: int,
    height_mm: float,
) -> Path:
    """Create a landscape book-folding guide and return its PDF path.

    The image is mapped across the odd-numbered pages in the inclusive page
    range. Each page is shown as a 5 mm-wide column with 2 mm between columns;
    black image areas become the fold marks inside the book-height guides.
    """
    if pageStart < 1 or pageStop < pageStart:
        raise ValueError("pageStart and pageStop must be positive and ordered")
    if height_mm <= 0:
        raise ValueError("height_mm must be greater than zero")

    first_odd_page = pageStart if pageStart % 2 else pageStart + 1
    page_numbers = list(range(first_odd_page, pageStop + 1, 2))
    if not page_numbers:
        raise ValueError("The page range must include at least one odd page")

    image_path = Path(img)
    if not image_path.is_file():
        raise FileNotFoundError(f"Image file not found: {image_path}")

    bar_width = 5 * mm
    bar_gap = 2 * mm
    column_pitch = bar_width + bar_gap
    margin_x = 12 * mm
    margin_bottom = 10 * mm
    height = height_mm * mm

    a4_width, a4_height = landscape(A4)
    page_height = max(a4_height, height + 24 * mm)
    page_width = max(a4_width, page_height + 1 * mm)
    columns_per_sheet = max(
        1,
        int((page_width - 2 * margin_x + bar_gap) // column_pitch),
    )
    pixel_height = max(1, round(height_mm * 4))

    with Image.open(image_path) as source:
        grayscale = source.convert("L")
        resized = grayscale.resize(
            (len(page_numbers), pixel_height),
            resample=Image.Resampling.LANCZOS,
        )
        pixels = resized.load()

        output_path = image_path.with_name(f"{image_path.stem}_faltmuster.pdf")
        pdf = canvas.Canvas(
            str(output_path),
            pagesize=(page_width, page_height),
        )
        pdf.setFillColorRGB(0, 0, 0)
        pdf.setStrokeColorRGB(0, 0, 0)
        pdf.setLineWidth(0.35)

        for first in range(0, len(page_numbers), columns_per_sheet):
            last = min(first + columns_per_sheet, len(page_numbers))
            count = last - first
            x_end = margin_x + count * bar_width + (count - 1) * bar_gap
            bottom_y = margin_bottom
            top_y = bottom_y + height

            pdf.line(margin_x, bottom_y, x_end, bottom_y)
            pdf.line(margin_x, top_y, x_end, top_y)

            for column, page_number in enumerate(page_numbers[first:last]):
                x = margin_x + column * column_pitch
                label = str(page_number)
                pdf.setFont("Helvetica", 7)
                label_width = pdf.stringWidth(label, "Helvetica", 7)
                font_size = min(7, 0.85 * column_pitch * 7 / label_width)
                pdf.setFont("Helvetica", font_size)
                pdf.drawCentredString(
                    x + bar_width / 2,
                    top_y + 3 * mm,
                    label,
                )

                runs = []
                run_start = None
                for row in range(pixel_height + 1):
                    is_dark = row < pixel_height and pixels[first + column, row] < 128
                    if is_dark and run_start is None:
                        run_start = row
                    elif not is_dark and run_start is not None:
                        runs.append((run_start, row))
                        run_start = None

                if runs:
                    selected_run = runs[(first + column) % len(runs)]
                    run_start, run_end = selected_run
                    run_height = (run_end - run_start) * height / pixel_height
                    y = top_y - run_end * height / pixel_height
                    pdf.rect(
                        x,
                        y,
                        bar_width,
                        run_height,
                        fill=1,
                        stroke=0,
                    )

            pdf.showPage()

        pdf.save()

    return output_path
