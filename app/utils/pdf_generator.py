from enum import Enum
from pathlib import Path

from fpdf import FPDF, HTMLMixin

from app.utils.text_transformation import execute_transformation_process

STATIC_FOLDER = Path('./app').resolve() / 'static'
FONTS_FOLDER = STATIC_FOLDER / 'fonts'
PDF_BACKGROUND_IMAGE = 'pdf_background.png'
BIONIC_READER_IMAGE = 'Bionic-Reader-img.jpg'
FOOTER_HTML_TEXT = (
            '<a href="https://bionic-reader.up.railway.app/">'
            'Bionic Reader</a><br />Developed by Igor'
            ' <a href="https://github.com/bnzone">@bnzone</a>'
            ' & Alexander <a href="https://github.com/simatheone">'
            '@simatheone</a>'
        )


class BackgroundImageProperties(Enum):
    NAME = STATIC_FOLDER / PDF_BACKGROUND_IMAGE
    X_COORD = 0
    Y_COORD = 0
    WIDTH = 210
    HEIGHT = 297
    ALT_TEXT = 'Grey Background'


class PDF(FPDF, HTMLMixin):
    def header(self):
        self.image(name=BackgroundImageProperties.NAME.value,
                   x=BackgroundImageProperties.X_COORD.value,
                   y=BackgroundImageProperties.Y_COORD.value,
                   w=BackgroundImageProperties.WIDTH.value,
                   h=BackgroundImageProperties.HEIGHT.value,
                   alt_text=BackgroundImageProperties.ALT_TEXT.value,)
        self.image(STATIC_FOLDER / BIONIC_READER_IMAGE,
                   x=10,
                   y=8,
                   w=33,
                   alt_text='Bionic Reader image',)
        self.ln(20)

    def create_pdf_body(self, transformed_text):
        font_path_inter_regular = (
            FONTS_FOLDER / 'Inter-Regular.ttf'
        ).as_posix()
        font_path_inter_bold = (FONTS_FOLDER / 'Inter-Bold.ttf').as_posix()
        self.add_page()

        self.add_font(fname=font_path_inter_bold, family='Inter', style='B')
        self.add_font(fname=font_path_inter_regular, family='Inter', style='')
        self.set_font('zapfdingbats', size=12)
        self.set_font('Inter', size=12)
        self.multi_cell(w=0,
                        h=10,
                        txt=transformed_text,
                        markdown=True,
                        new_x="LMARGIN",
                        new_y="NEXT",)

    def footer(self):
        self.set_font('Times', 'B', size=8)
        self.set_x(0)
        self.set_y(-8)
        self.write_html(FOOTER_HTML_TEXT)

        self.set_y(-7)
        self.set_font('Times', 'B', size=10)
        self.cell(w=0, h=0, txt=f'Page {self.page_no()}', align='C')


async def execute_pdf_generation_process(text_to_transform: str):
    transformed_text = await execute_transformation_process(
        text_to_transform, output_type='markdown'
    )
    try:
        new_pdf = PDF()
        new_pdf.create_pdf_body(transformed_text)
        pdf_file = new_pdf.output()
        return pdf_file
    except Exception:
        return b''
