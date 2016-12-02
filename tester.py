from weasyprint import HTML

URL = "http://193.67.229.68:8000/powerview/_troubleshooting/index.html"
OUT = "/home/admin-s/test.pdf"

for lp in range(0, 300):
    print(str(lp))
    HTML(URL).write_pdf(OUT)
