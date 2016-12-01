#!/usr/bin/env python

import io
import logging
from flask import Flask, request
from flask.helpers import send_file
from weasyprint import HTML

from werkzeug.exceptions import abort

#from fakeHTML import HTML
from logger.mylogger import setup_logging

lgr = logging.getLogger(__name__)
app = Flask('pdf')


@app.route('/health')
def index():
    return 'ok'

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
    lgr.debug("url to pdf: {}".format(url))
    if url is not None:
        try:
            html = HTML(url)
        except Exception as e:
            lgr.exception()
            abort(404)
        #img_io = StringIO() #2.7
        img_io=io.BytesIO()  #3.5
        try:
            html.write_pdf(img_io)
        except Exception as e:
            lgr.exception()
            img_io.close()
            abort(404)
        else:
            img_io.seek(0)

            return send_file(img_io,
                             mimetype='pdf',
                             as_attachment=True,
                             attachment_filename="generated_pdf.pdf")



if __name__ == '__main__':
    setup_logging("logger/log_config.json")
    lgr = logging.getLogger(__name__)
    lgr.debug("starting.....")
    app.run(port=5001, host="0.0.0.0")
