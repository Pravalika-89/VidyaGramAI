from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


def generate_pdf(prediction, info, roadmap, filename="career_report.pdf"):

    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("VidyaGram AI - Career Report", styles["Title"]))
    elements.append(Paragraph("<br/>", styles["Normal"]))

    elements.append(Paragraph(f"<b>Career:</b> {prediction}", styles["Heading2"]))

    if info:
        elements.append(Paragraph(f"<b>Description:</b> {info.get('description', 'N/A')}", styles["BodyText"]))
        elements.append(Paragraph(f"<b>Salary:</b> {info.get('salary', 'N/A')}", styles["BodyText"]))

        elements.append(Paragraph("<br/><b>Required Skills:</b>", styles["Heading2"]))
        for skill in info.get("skills", []):
            elements.append(Paragraph(f"• {skill}", styles["BodyText"]))

        elements.append(Paragraph("<br/><b>Recommended Courses:</b>", styles["Heading2"]))
        for course in info.get("courses", []):
            elements.append(Paragraph(f"• {course}", styles["BodyText"]))

    if roadmap:
        elements.append(Paragraph("<br/><b>Career Roadmap:</b>", styles["Heading2"]))
        for i, step in enumerate(roadmap, start=1):
            elements.append(Paragraph(f"{i}. {step}", styles["BodyText"]))

    doc.build(elements)

    return filename