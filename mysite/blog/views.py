from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, Http404
from django.shortcuts import get_object_or_404
from .models import Post


def post_list(request: HttpRequest) -> HttpResponse:
    posts = Post.published.all()

    return render(
        request,
        'blog/post/list.html',
        {'posts': posts}
    )


def post_detail(request: HttpRequest, id: int) -> HttpResponse:
    # вариант 1
    #try:
    #    post = Post.published.get(id=id)
    #except Post.DoesNotExist:
    #    raise Http404("No Post found.")

    # вариант 2
    post = get_object_or_404(Post, id=id, status=Post.Status.PUBLISHED)

    return render(
        request,
        'blog/post/detail.html',
        {'post': post}
    )
