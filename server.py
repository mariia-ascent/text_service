#!/usr/bin/env python3

import os
import sys

import http.server
from http.server import BaseHTTPRequestHandler
import socketserver
import requests
import json
import html
from datetime import datetime

import momotools as momo
from momotools import logging
from momotools import data
logger = logging.Logger.getLogger()

# import transformers
# import spacy

# nlp = spacy.load("de_core_news_sm")

HOSTNAME = 'localhost'
PORTNO = 8090

class PredictServer(BaseHTTPRequestHandler):

  khiz2id = {}   # map KHIZ on mongo-DB key


  def respond200(self, response_as_string):
    # send response
    self.send_response(200);
    self.send_header('Content-type', 'text')
    self.end_headers()
    self.wfile.write(bytes(response_as_string, "UTF-8"))

  def nlp_text(self, text):
    doc = nlp(text)
    return doc.text()

  def do_GET(self):
    self.send_response(400)
    self.send_header('Content-type', 'text')
    self.end_headers()
    self.wfile.write(bytes("Kein get moeglich, nur POST", "UTF-8"))
    return

  def do_POST(self):

    print("received request url:" + self.path);
    body_as_string = ''
    url = str(self.path)

    try :

      # read body
      content_length = int(self.headers.get('content-length', 0))
      logger.debug("content length:" + str(content_length));
      body = self.rfile.read(content_length)
      body_as_string = body.decode()  # from bytes[] to string ???
      body_as_string = data.atob(body_as_string, "request")
      if len(body_as_string)>0:
        requestAsDict = json.loads(body_as_string)

      # call the handler as defined by the url
      response_as_string = None

      if self.path == "/hello":
        response_as_string = "Hallo aus Microservice text_service um " + str(datetime.now())
        self.respond200(data.btoa(response_as_string, "response"))

      elif self.path == "/predict":
        requestAsDict = "SPACY:"+self.nlp_text(requestAsDict['report'])
        response = {
          "msg" : "Your report is: " + requestAsDict
        }
        response_as_string =  json.dumps(response)
        response_as_string =  data.btoa(response_as_string, "response")
        self.respond200(response_as_string)

      else : # type(response_as_string) == type(None):
        raise Exception("no such url: " + self.path );

    except Exception as e:

      logger.errorTime_(str(e), -2);
      logger.flush()
      self.send_response(400)
      self.send_header('Content-type', 'text')
      self.end_headers()
      self.wfile.write(bytes(str(e), "UTF-8"))

    return

if __name__ == '__main__':

  # init: set portno if given (otherwise default = 8090
  if len(sys.argv) == 2:
    PORTNO = int(sys.argv[1])

  Handler = PredictServer # http.server.SimpleHTTPRequestHandler
  httpd = socketserver.TCPServer((HOSTNAME, PORTNO), Handler)
  print("start server at port: " + str(PORTNO))
  httpd.serve_forever()
