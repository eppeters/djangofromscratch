"""
WSGI config for dfsdjango project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dfsdjango.settings")


def trace_wsgi(environ, start_response):
    import sys
    import trace

    print(sys.prefix, sys.exec_prefix)

    # create a Trace object, telling it what to ignore, and whether to
    # do tracing or line-counting or both.
    tracer = trace.Trace(
        trace=1,
        count=0)

    from io import StringIO
    old_stdout = sys.stdout
    sys.stdout = mystdout = StringIO()
    # run the new command using the given tracer
    wsgi_return = tracer.runfunc(get_wsgi_application(), environ, start_response)
    sys.stdout = old_stdout
    out = mystdout.getvalue()
    outfile = open('trace.out', 'a+')
    outfile.write('=======================EDDIETRACE=========================\n')
    outfile.write(out)
    outfile.close()

    # make a report, placing output in the current directory
    r = tracer.results()
    r.write_results(show_missing=True, coverdir=".")

    return wsgi_return


def wsgi_app(environ, start_response):
    return trace_wsgi(environ, start_response)


application = wsgi_app
