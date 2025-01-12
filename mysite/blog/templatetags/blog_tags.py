from django import template
from django.utils.safestring import mark_safe
from django.db.models import Count, QuerySet
import markdown
from ..models import Post

register = template.Library()  # используется для регистрации шаблонных тегов и фильтров приложения


@register.simple_tag
def total_posts() -> int:
    """Возвращает общее число опубликованных постов."""
    return Post.published.count()


@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count: int = 5) -> dict:
    """
    Возвращает словарь с указанным количеством опубликованных постов,
    отсортированные по дате публикации.
    """

    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


@register.simple_tag
def get_most_commented_posts(count=5) -> QuerySet:
    """Возвращает QuerySet с указанным количеством опубликованных и самых комментируемых постов"""
    return Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]


@register.filter(name='markdown')
def markdown_format(text):
    """Фильтр, поддерживающий разметку Markdown"""
    return mark_safe(markdown.markdown(text))
