  from fpdf import FPDF
  from reportlab.pdfgen import canvas


  def export_to_pdf(users_data):

    pdf_filename = "streak_report.pdf"
    c = canvas.Canvas(pdf_filename)

    # Add content to the PDF
    c.drawString(100, 750, "Streak Completion Report")
    y_position = 700

    for user_data in users_data:
        user_id = user_data["_id"]
         #Add user information to the PDF
        c.drawString(100, y_position, f"User ID: {user_id}")
        y_position -= 20

    # Save the PDF file
    c.save()
    return pdf_filename

