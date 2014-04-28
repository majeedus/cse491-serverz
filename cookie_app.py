def wsgi_app(environ, start_response):
    path = environ['PATH_INFO']

    if path == '/':
        info = environ.get('HTTP_COOKIE', "")
        info = "COokie Info: %s<p>" % info

        start_response('200 OK', [('Content-type', 'text/html')])
        return [info,
                "<a href='/set'>Set Cookie</a> | ",
                "<a href='/del'>Clear Cookie</a>"]
    elif path == '/set':
        start_response('302 Redirect', [
            ('Location', '/'),
            ('Set-Cookie', 'my_template=green')
            ])

        return ["You should be redirected"]
    elif path == '/del':
        start_response('302 Redirect', [
            ('Location', '/'),
            ('Set-Cookie', 'my_template=NONE; Expires=Thu, 01-Jan-1970 00:00:01 GMT')
            ])

        return ["You should be redirected"]

    start_response('404 Not Found', [])
    return []
