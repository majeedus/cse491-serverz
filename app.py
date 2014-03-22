from wsgiref.util import setup_testing_defaults
import StringIO
import jinja2
import urlparse
import cgi
import sys

class my_app:
	def _init_(self):
	# Initiate the jinja2 environment and loader
		loader = jinja2.FileSystemLoader('./templates')
		self.env = jinja2.Environment(autoescape=False, extensions=['jinja2.ext.autoescape'], loader=loader)
		self.output = []
	
	def run_app(self, environ, start_response):
		path = environ['PATH INFO']
		query = environ['QUERY_STRING']
		request = environ['REQUEST_METHOD']
		wsgi_input = environ['wsgi.input']
		content_type = ['CONTENT_TYPE']
		content_len = ['CONTENT_LENGTH']
		
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

		if request == 'GET':
			if path == '/':
				self.index()
			elif path == '/content':
				self.content()
			elif path == '/file':
				self.file()
			elif path == '/image':
				self.image()
			elif path == '/form':
				self.form()
			elif path == '/formpost':
				self.form_post()
			elif path == '/submit':
				self.get_submit(query)
			else:
				status = '404 Not Found'
				self.send404()
		elif request == 'POST':
			self.post(content_len, content_type, wsgi_input, environ)

		start_response(status, response_headers)
		return self.output
	
	#def send200(conn):
		#return self.output.append['HTTP1.0 200 OK \r\n']
	    
	def send404(environ):
	    return '404 NOT FOUND', [('Content-type', 'text/html')], \
	    env.get_template('error404.html').render({'PATH': environ['PATH_INFO']}).encode('latin-1', 'replace')
	
	def send501(environ):
	    return '501 NOT IMPLEMENTED', [('Content-type', 'text/html')], \
	    env.get_template('error501.html').render({'PATH': environ['PATH_INFO']}).encode('latin-1', 'replace')
	
	def index(self):
		vars = dict(title='Index')
		data = self.env.get_template('index.html').render(vars).encode('latin-1', 'replace')
		self.output = []
		self.output.append(content)
	
	def content(self):
		vars = dict(title='Content')
		data = data = self.env.get_template('content.html').render(vars).encode('latin-1', 'replace')
		self.output = []
		self.outpout.append(content)
		
	def image(self):
		vars = dict(title='Image')
		data = self.env.get_template('image.html').render(vars).encode('latin-1', 'replace')
		self.output = []
		img = open_file("images/dogecoin.jpg")
	    
	def file(self):
		vars = dict(title='File')
		data = self.env.get_template('file.html').render(vars).encode('latin-1', 'replace')
		self.output = []
		self.output.append(data)
		self.serve_file()
	
	def form(self):
		vars = dict(title='Form')
		data = self.env.get_template('form.html').render(vars).encode('latin-1', 'replace')
		self.output = []
		self.output.append(data)
	        
	def form_post(environ):
	    return '200 OK', [('Content-type','text/html')], \
	    env.get_template('form_post.html').render().encode('latin-1', 'replace')
				 
	def get_submit(self, query):
		data = urlprase.parse_qs(query)
		try:
			firstname = data['firstname'][0]
		except KeyError:
			firstname = ''
		try:
			lastname = data['lastname'][0]
		except KeyError:
			lastname = ''
		
		vars = dict(firstname=firstname, lastname=lastname, title='Get')
		output = self.env.get_template('form_results.html').render(vars).encode('latin-1', 'replace')
		self.output = []
		self.output.append(output)
	        
	#def post_results(form):
	    #query = {'firstname':form.getvalue('firstname'), 'lastname':form.getvalue('lastname')}
	    
	    #return '200 OK', [('Content-type', 'text/html')], \
	    #env.get_template('form_results.html').render(query).encode('latin-1', 'replace')
	    
	def post(self, content_len, content_type, wsgi_input, environ):
		post_dict = []
		cgi_type = 'Content-Length: ' + str(contentLength)
		cgi_len = 'Content-Type: ' + contentType
		post_dict.append(cgi_type)
		post_dict.append(cgi_len)
		
		dict2 = {}
		if 'multipart' in contentType:
			for line in d:
				k, v = line.split(': ', 1)
				dict2[k.lower()] = v
	
		form = cgi.FieldStorage(
			headers = dict2,
			fp=wsgiInput,
			environ=environ
		)
		try:
			firstname = form['firstname'].value
		except KeyError:
			firstname = ''
		try:
			lastname = form['lastname'].value
		except KeyError:
			lastname = ''
		vars = dict(firstname=firstname, lastname=lastname, title='Post')
		data = self.env.get_template('submit_post.html').render(vars).encode('latin-1', 'replace')
		self.output = []
		self.output.append(data)
	    
	def open_file(filename):
	    fp = open(filename, "rb")
	    data = fp.read()
	    fp.close()
	    return data

def create_app():
	app = my_app()
	return app.start_app
