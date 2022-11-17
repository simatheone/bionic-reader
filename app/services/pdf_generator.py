from pathlib import Path

from fpdf import FPDF, HTMLMixin

from app.services.text_transformation import execute_transformation_process

STATIC_FOLDER = Path('./app').resolve() / 'static'
FONTS_FOLDER = STATIC_FOLDER / 'fonts'
PDF_BACKGROUND_IMAGE = 'pdf_background.png'
BIONIC_READER_IMAGE = 'Bionic-Reader-img.jpg'


class PDF(FPDF, HTMLMixin):
    def header(self):
        self.image(
            STATIC_FOLDER / PDF_BACKGROUND_IMAGE,
            x=0,
            y=0,
            w=210,
            h=297,
            alt_text='grey background',
        )
        self.image(
            STATIC_FOLDER / BIONIC_READER_IMAGE,
            x=10,
            y=8,
            w=33,
            alt_text='Bionic Reader image',
        )
        self.ln(20)

    def create_pdf_body(self, transformed_text):
        font_path_inter_regular = (FONTS_FOLDER / 'Inter-Regular.ttf').as_posix()
        font_path_inter_bold = (FONTS_FOLDER / 'Inter-Bold.ttf').as_posix()
        self.add_page()

        self.add_font(fname=font_path_inter_bold, family='Inter', style='B')
        self.add_font(fname=font_path_inter_regular, family='Inter', style='')
        self.set_font('zapfdingbats', size=12)
        self.set_font('Inter', size=12)
        self.multi_cell(
            w=0,
            h=10,
            txt=transformed_text,
            markdown=True,
            new_x="LMARGIN",
            new_y="NEXT",
        )

    def footer(self):
        self.set_font('Times', 'B', size=8)
        self.set_x(0)
        self.set_y(-8)
        footer_html_text = (
            '<a href="https://bionic-reader.up.railway.app/">'
            'Bionic Reader</a><br />Developed by Igor'
            ' <a href="https://github.com/bnzone">@bnzone</a>'
            ' & Alexander <a href="https://github.com/simatheone">'
            '@simatheone</a>'
        )
        self.write_html(footer_html_text)

        self.set_y(-7)
        self.set_font('Times', 'B', size=10)
        self.cell(0, 0, f'Page {self.page_no()}', align='C')


async def execute_pdf_generation_process(text_to_transform: str):
    transformed_text = await execute_transformation_process(
        text_to_transform, output_type='markdown'
    )
    new_pdf = PDF()
    new_pdf.create_pdf_body(transformed_text)
    pdf_file = new_pdf.output()
    return pdf_file
