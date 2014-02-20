from wsgiref.util import setup_testing_defaults
import StringIO
import jinja2
import urlparse
import cgi
import sys

# Initiate the jinja2 environment and loader
loader = jinja2.FileSystemLoader('./templates')
env = jinja2.Environment(autoescape=False, extensions=['jinja2.ext.autoescape'], loader=loader)

def app(environ, start_response):
	setup_testing_defaults(environ)

	status = '200 OK'
	response_headers = [('Content-type', 'text/html')]
	response = ''
	if environ['REQUEST_METHOD'] == 'GET':
		status, response_headers, response = getRequest(environ)
	elif environ['REQUEST_METHOD'] == 'POST':
		status, response_headers, response = postRequest(environ)
		if "multipart/form-data" in environ['CONTENT_TYPE']:
			cLen = int(environ['CONTENT_LENGTH'])
			data = environ['wsgi.input'].read(cLen)
			environ['wsgi.input'] = StringIO(data)
	else:
		status, response_headers, response = send501(environ)

	start_response(status, response_headers)
	return response
	
def getRequest(environ):	
    if environ['PATH_INFO'] == '/':
        return index(environ)
    elif environ['PATH_INFO'] == '/content':
        return content(environ)
    elif environ['PATH_INFO'] == '/file':
        return file(environ)
    elif environ['PATH_INFO'] == '/image':
        return image(environ)
    elif environ['PATH_INFO'] == '/form':
        return form(environ)
    elif environ['PATH_INFO'] == '/formpost':
        return form_post(environ)
    elif environ['PATH_INFO'] == '/submit':
        return get_results(environ)
    else:
        return send404(environ)


def postRequest(environ):
	form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)
	if environ['PATH_INFO'] == '/submitpost':
		return post_results(form)
	else:
		return send404(environ)

#def send200(conn):
    #conn.send('HTTP/1.0 200 OK\r\n')
    #conn.send('Content-type: text/html\r\n')
    #conn.send('\r\n')
    
def send404(environ):
    return '404 NOT FOUND', [('Content-type', 'text/html')], \
    env.get_template('error404.html').render({'PATH': environ['PATH_INFO']}).encode('latin-1', 'replace')

def send501(environ):
    return '501 NOT IMPLEMENTED', [('Content-type', 'text/html')], \
    env.get_template('error501.html').render({'PATH': environ['PATH_INFO']}).encode('latin-1', 'replace')

def index(environ):
    return '200 OK', [('Content-type','text/html')], \
    env.get_template('index.html').render().encode('latin-1', 'replace')

def content(environ):
    return '200 OK', [('Content-type','text/html')], \
    env.get_template('content.html').render().encode('latin-1', 'replace')

def image(environ):
	img = open_file("images/dogecoin.jpg")
	return '200 OK', [('Content-type','image/jpeg')], img
    
def file(environ):
    txtfile = open_file("files/foo_bar.txt")
    return '200 OK', [('Content-type','text/plain')], txtfile

def form(environ):
    return '200 OK', [('Content-type','text/html')], \
    env.get_template('form.html').render().encode('latin-1', 'replace')
	
def form_post(environ):
    return '200 OK', [('Content-type','text/html')], \
    env.get_template('form_post.html').render().encode('latin-1', 'replace')
			 
def get_results(environ):
    query_string = urlparse.parse_qs(environ['QUERY_STRING'])
    query = {'firstname':query_string['firstname'][0], 'lastname':query_string['lastname'][0]}

    return '200 OK', [('Content-type', 'text/html')], \
    env.get_template('form_results.html').render(query).encode('latin-1', 'replace')

def post_results(form):
    query = {'firstname':form.getvalue('firstname'), 'lastname':form.getvalue('lastname')}
    
    return '200 OK', [('Content-type', 'text/html')], \
    env.get_template('form_results.html').render(query).encode('latin-1', 'replace')
    
def open_file(filename):
    fp = open(filename, "rb")
    data = fp.read()
    fp.close()
    return data
	

def create_app():
	return app
