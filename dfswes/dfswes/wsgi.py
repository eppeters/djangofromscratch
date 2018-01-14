"""
WSGI config for dfswes project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""


def trace_wsgi(environ, start_response):
    import sys
    import trace

    print(sys.prefix, sys.exec_prefix)

    # create a Trace object, telling it what to ignore, and whether to
    # do tracing or line-counting or both.
    tracer = trace.Trace(
        ignoredirs=[sys.prefix, sys.exec_prefix],
        trace=1,
        count=1,
        outfile='out.trace')

    # run the new command using the given tracer
    wsgi_return = tracer.runfunc(wsgi_app, environ, start_response)

    # make a report, placing output in the current directory
    r = tracer.results()
    r.write_results(show_missing=True, coverdir=".")

    return wsgi_return


def wsgi_app(environ, start_response):
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain')]
    start_response(status, response_headers)
    return [b'Hello world!\n\t- Love, Wes']

application = trace_wsgi
