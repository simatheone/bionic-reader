from fpdf import FPDF

from app.services.text_transformation import execute_transformation_process


class PDF(FPDF):
    def header(self):
        self.image(
            'background_for_pdf.png',
            x=0,
            y=0,
            w=210,
            h=297
        )
        self.image(
            'Bionic-Reader-img.jpg',
            x=10,
            y=8,
            w=33,
            title='Bionic Reader image'
        )
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Times', 'B', size=10)
        self.cell(0, 0, f'{self.page_no()}', align='C')


async def execute_pdf_generation_process(
    text_to_transform: str,
    doc_title: str
):
    transformed_text = await execute_transformation_process(
        text_to_transform
    )
    new_pdf = PDF()
    new_pdf.add_page()
    new_pdf.set_font('Times', size=14)
    new_pdf.multi_cell(
        w=0,
        h=10,
        txt=transformed_text,
        markdown=True,
        new_x="LMARGIN",
        new_y="NEXT"
    )
    return new_pdf.output(f'{doc_title}.pdf')
