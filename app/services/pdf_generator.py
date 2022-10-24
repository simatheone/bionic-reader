from pathlib import Path

from fpdf import FPDF

from app.services.text_transformation import execute_transformation_process

BASE_DIR = Path(__file__).parent.parent
STATIC_FOLDER = BASE_DIR.joinpath('static')


class PDF(FPDF):
    def header(self):
        self.image(
            STATIC_FOLDER.joinpath('pdf_background.png'),
            x=0,
            y=0,
            w=210,
            h=297
        )
        self.image(
            STATIC_FOLDER.joinpath('Bionic-Reader-img.jpg'),
            x=10,
            y=8,
            w=33,
            title='Bionic Reader image'
        )
        self.ln(20)

    def footer(self):
        self.set_y(-15)
        self.set_font('Times', 'B', size=10)
        self.cell(0, 0, f'{self.page_no()}', align='C')


async def execute_pdf_generation_process(
    text_to_transform: str
):
    transformed_text = await execute_transformation_process(
        text_to_transform,
        output_type='markdown'
    )
    new_pdf = PDF()
    new_pdf.add_page()
    # Add try/except that pdf builds with that text font
    # pdf.errors.FPDFUnicodeEncodingException: Character "’"
    # at index 389 in text is outside the range of characters supported
    # by the font used: "times". Please consider using a Unicode font.
    # new_pdf.set_font('Times', size=14)
    new_pdf.set_font('Latin-1', size=14)
    new_pdf.multi_cell(
        w=0,
        h=10,
        txt=transformed_text,
        markdown=True,
        new_x="LMARGIN",
        new_y="NEXT"
    )
    pdf_file = new_pdf.output()
    return pdf_file
