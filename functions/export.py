from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import io

def dataframe_to_pdf_bytes(df, username):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Define the starting point for the title
    c.setFont("Helvetica-Bold", 16)  # Set font size and style
    title_x = 50
    title_y = height - 50
    title_text = "Messdaten von: {}".format(username)
    c.drawString(title_x, title_y, title_text)

    # Define the starting point for the DataFrame
    x_offset = 50
    y_offset = height - 100
    line_height = 20


    # Set font for headers to bold
    c.setFont("Helvetica-Bold", 14)

    # Draw the DataFrame headers
    for col_num, column in enumerate(df.columns):
        c.drawString(x_offset + col_num * 100, y_offset, str(column))

     # Set font for the rest of the text
    c.setFont("Helvetica", 12)

    # Draw the DataFrame rows
    for row_num, row in df.iterrows():
        for col_num, cell in enumerate(row):
            c.drawString(x_offset + col_num * 100, y_offset - (row_num + 1) * line_height, str(cell))

    c.save()
    buffer.seek(0)

    return buffer.read()