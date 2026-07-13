from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


def generate_resume(name, email, phone, education, skills, projects,
                    filename="resume.pdf"):

    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("<b>RESUME</b>", styles["Title"]))

    elements.append(Paragraph(f"<b>Name:</b> {name}", styles["BodyText"]))
    elements.append(Paragraph(f"<b>Email:</b> {email}", styles["BodyText"]))
    elements.append(Paragraph(f"<b>Phone:</b> {phone}", styles["BodyText"]))

    elements.append(Paragraph("<br/><b>Education</b>", styles["Heading2"]))
    elements.append(Paragraph(education, styles["BodyText"]))

    elements.append(Paragraph("<br/><b>Skills</b>", styles["Heading2"]))
    elements.append(Paragraph(skills, styles["BodyText"]))

    elements.append(Paragraph("<br/><b>Projects</b>", styles["Heading2"]))
    elements.append(Paragraph(projects, styles["BodyText"]))

    doc.build(elements)

    return filename