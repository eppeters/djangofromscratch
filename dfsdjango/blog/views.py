from io import BytesIO

import markdown

from django.shortcuts import render
from django.http import HttpResponse

from dfsdjango import settings

def homepage(request):
    content_html = BytesIO()
    markdown.markdownFromFile('{}/../README.md'.format(settings.BASE_DIR), content_html)
    content_html = content_html.getvalue().decode('UTF-8')
    context = { 'content':  content_html }
    return render(request, 'blog/homepage.html', context)
