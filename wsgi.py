#!/usr/bin/env python
import StringIO
import logging

from flask import Flask, request
from flask.helpers import send_file
from weasyprint import HTML
from werkzeug.exceptions import abort
lgr = logging.getLogger(__name__)
app = Flask('pdf')


@app.route('/health')
def index():
    return 'ok'


@app.before_first_request
def setup_logging():
    logging.addLevelName(logging.DEBUG, "\033[1;36m%s\033[1;0m" % logging.getLevelName(logging.DEBUG))
    logging.addLevelName(logging.INFO, "\033[1;32m%s\033[1;0m" % logging.getLevelName(logging.INFO))
    logging.addLevelName(logging.WARNING, "\033[1;33m%s\033[1;0m" % logging.getLevelName(logging.WARNING))
    logging.addLevelName(logging.ERROR, "\033[1;31m%s\033[1;0m" % logging.getLevelName(logging.ERROR))

    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'
    ))
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.DEBUG)


@app.route('/')
def home():
    return '''
        <h1>PDF Generator</h1>
        <p>The following endpoints are available:</p>
        <ul>
            <li>POST to <code>/pdf?filename=myfile.pdf</code>. The body should
                contain html</li>
            <li>POST to <code>/multiple?filename=myfile.pdf</code>. The body
                should contain a JSON list of html strings. They will each
                be rendered and combined into a single pdf</li>
        </ul>
    '''


@app.route('/url', methods=['GET'])
def get_from_url():
    url = request.args.get('url')
    if url is not None:
        try:
            html = HTML(url)
        except Exception as e:
            abort(404)
            lgr.error("Unable getting html from: {}".format(url))
        img_io = StringIO.StringIO()
        try:
            html.write_pdf(img_io)
        except MemoryError as e:
            lgr.error("Unable to create pdf from: {}".format(url))
            abort(404)
        except Exception as e:
            lgr.error("Unable to create pdf from: {}".format(url))
            lgr.error(e)
            abort(404)

        img_io.seek(0)

        return send_file(img_io,
                         mimetype='pdf',
                         as_attachment=True,
                         attachment_filename="generated_pdf.pdf")


if __name__ == '__main__':
    app.run(port=5001, host="0.0.0.0")
