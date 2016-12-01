from weasyprint import HTML

URL = "http://www.google.com/"
OUT = "/home/admin-s/test.pdf"

for lp in range(0, 300):
    print(str(lp))
    HTML(URL).write_pdf(OUT)
