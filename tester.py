from weasyprint import HTML
import logging

logging.basicConfig(level=logging.DEBUG)

URL = "http://tools.hde.nl/menc/site/guides/Pliss%C3%A9%20%26%20Duette%C2%AE%20Bottom-Up%20programming/"
OUT = "/home/admin-s/test.pdf"

for lp in range(0, 300):
    try:
        HTML(URL).write_pdf(OUT)
    except OSError as e:
        logging.exception("**************** ERROR AT ATTEMPT: {} *******************".format(lp))
        break
