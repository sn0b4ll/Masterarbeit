#!/usr/bin/env python
"""
    Simple script to start mitmproxy up and write req, resp and log to a specified file line by line
"""
import argparse
import json
import signal
import sys

from mitmproxy import flow, controller, options
from mitmproxy.proxy import ProxyServer, ProxyConfig

class MyMaster(flow.FlowMaster):
    log_file = ""

    def run(self):
        try:
            flow.FlowMaster.run(self)
        except KeyboardInterrupt:
            self.shutdown()

    @controller.handler
    def request(self, f):
        req_dic = { 'type' : 'request' }
        req_dic['content'] = f.request.content
        req_dic['headers'] = f.request.headers
        req_dic['cookies'] = f.request.cookies
        self.log_file.write(json.dumps(str(req_dic)) + "\n")
        self.log_file.flush()


    @controller.handler
    def response(self, f):
        resp_dic = { 'type' : 'response'}
        resp_dic['content'] = f.response.content
        resp_dic['headers'] = f.response.headers
        resp_dic['cookies'] = f.response.cookies
        self.log_file.write(json.dumps(str(resp_dic)) + "\n")
        self.log_file.flush()

    @controller.handler
    def error(self, f):
        print("error", f)
        print(dir(f))

    @controller.handler
    def log(self, l):
        log_dic = { 'type' : 'log'}
        log_dic['level'] = l.level
        log_dic['msg'] = l.msg
        log_dic['reply'] = l.reply
        self.log_file.write(json.dumps(str(log_dic)) + "\n")
        self.log_file.flush()

    def set_log_file(self, log_file):
        self.log_file = log_file


def start_mitm_proxy(log_file):
    opts = options.Options(cadir="~/.mitmproxy/")
    config = ProxyConfig(opts)
    state = flow.State()
    server = ProxyServer(config)

    log_file = open(log_file, 'w')

    m = MyMaster(opts, server, state)
    m.set_log_file(log_file)
    m.run()
    log_file.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Capture mitmproxy traffic to file.')
    parser.add_argument('--file', metavar='file', help='the file to write to', required=True)
    args = parser.parse_args()

    start_mitm_proxy(args.file)
