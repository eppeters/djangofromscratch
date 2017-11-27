from io import BytesIO

import markdown

from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .forms import CommentForm
from .models import Comment

@csrf_exempt
def homepage(request):
    if request.method == 'POST':
        return handle_homepage_post(request)
    else:
        return handle_homepage_get(request)

def handle_homepage_post(request):
    form = CommentForm(request.POST)
    if form.is_valid():
        new_comment = Comment(
                body=form.cleaned_data['body'],
                author=form.cleaned_data['author'])
        new_comment.save()
    return HttpResponseRedirect(reverse('homepage'))

def handle_homepage_get(request):
    content_html = BytesIO()
    markdown.markdownFromFile('{}/README.md'.format(settings.BASE_DIR), content_html)
    content_html = content_html.getvalue().decode('UTF-8')
    comments = Comment.objects.order_by('-id').all()
    context = { 'content':  content_html, 'form': CommentForm(), 'comments': comments, 'framework': 'Django' }
    return render(request, 'blog/homepage.html', context)
