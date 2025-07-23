from scripts import *

pdf_path = "IMO class 1 Maths Olympiad Sample Paper 1 for the year 2024-25.pdf"

content = extract_content_from_pdf(pdf_path)

questions = generate_questions(content)

