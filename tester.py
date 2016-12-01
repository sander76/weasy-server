from weasyprint import HTML

URL = "http://www.google.com/"
OUT = "~/test.pdf"

for lp in range(0, 200):
    HTML(URL).write_pdf(OUT)
