from fpdf import FPDF

def export_to_pdf(streaks):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="List of Eligible Participants", ln=True, align='C')

    for user_id in streaks:
      if streaks[user_id] ==30:
        pdf.cell(200, 10, txt=f"User ID: {user_id}, Streak: {streaks[user_id]}", ln=True, align='L')

    pdf.output("eligible_participants.pdf")