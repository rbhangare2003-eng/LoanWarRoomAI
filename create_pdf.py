from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

doc = SimpleDocTemplate("sample_loan.pdf")
elements = []

styles = getSampleStyleSheet()
text = """
Revenue: 5000000
EBITDA: 1200000
Debt: 2000000
Equity: 3000000
Interest: 200000
"""

elements.append(Paragraph(text, styles["Normal"]))
doc.build(elements)

print("PDF created successfully!")
