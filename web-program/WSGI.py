'''
Created on Feb 21, 2016

@author: xuyi
'''
from wsgiref.simple_server import make_server

def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    body = '<h1>Hello, %s!</h1>' % (environ['PATH_INFO'][1:] or 'web')
    return [body.encode('utf-8')]

if __name__ == '__main__':
    httpd = make_server('', 9999, application)
    print('Serving HTTP on port 9999...')
    httpd.serve_forever()
    pass