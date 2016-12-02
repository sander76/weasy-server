from weasyprint import HTML

URL = "http://tools.hde.nl/menc/site/guides/Pliss%C3%A9%20%26%20Duette%C2%AE%20Bottom-Up%20programming/"
OUT = "/home/admin-s/test.pdf"

for lp in range(0, 300):
    print(str(lp))
    HTML(URL).write_pdf(OUT)
