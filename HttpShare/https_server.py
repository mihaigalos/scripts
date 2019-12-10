#!/usr/bin/env python
# based on work from Chase Schultz : https://github.com/f47h3r/basic-auth-simple-https-server

import os
import sys
import ssl
import logging
import http.server
from base64 import b64decode
import base64

logging.basicConfig(filename='server.log', level=logging.DEBUG)
logger = logging.getLogger()


class BasicAuthHandler(http.server.SimpleHTTPRequestHandler):

    key = ""
    @staticmethod
    def set_key(user_pass):
        BasicAuthHandler.key = base64.b64encode(user_pass.encode("utf-8"))

    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_AUTHHEAD(self):
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic')
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        try:
            if self.headers.get('Authorization') is None:
                self.do_AUTHHEAD()
                logger.debug('Auth Header Not Found')
                self.wfile.write(bytes('Unauthorized', 'utf8'))
            elif self.headers.get('Authorization') \
                    == ('Basic ' + self.key.decode("utf-8")):
                http.server.SimpleHTTPRequestHandler.do_GET(self)
            else:
                self.do_AUTHHEAD()
                auth_header = self.headers.get('Authorization')

                if len(auth_header.split(' ')) > 1:
                    logger.debug(auth_header.split(' ')[1])
                    logger.debug(b64decode(auth_header.split(' ')[1]))
                logger.debug('Bad Creds')
                self.wfile.write(bytes('Unauthorized', 'utf8'))
        except Exception:
            logger.error("Error in GET Functionality", exc_info=True)

    def date_time_string(self, time_fmt='%s'):
        return ''

    def log_message(self, format, *args):
        logger.debug("%s - - [%s] %s" % (
            self.client_address[0],
            self.log_date_time_string(),
            format % args))


if __name__ == '__main__':
    argv = sys.argv[1:]

    folder, port, certificate_file, user_pass = (
        argv[0], int(argv[1]), argv[2], argv[3])

    if not os.path.isfile('/server_certificate.pem'):
        error_message = """\n
/server_certificate.pem is missing. Try rerunning install.sh
"""
        raise Exception(error_message)

    handler = BasicAuthHandler
    BasicAuthHandler.set_key(user_pass)

    httpd = http.server.HTTPServer(('0.0.0.0', port), handler)
    httpd.socket = ssl.wrap_socket(
        httpd.socket, certfile=certificate_file, server_side=True)
    try:
        os.chdir(folder)
        httpd.serve_forever()
    except Exception:
        logger.error("Fatal error in main loop", exc_info=True)
