from django.contrib.sitemaps import Sitemap
from .models import Post


class PostSitemap(Sitemap):
    """Конкретно-прикладная карта сайта"""
    changefreq = 'weekly'
    priority = 0.9

    def items(self) -> 'QuerySet':
        """
        Возвращает все опубликованные посты в формате URL-адреса
        (Django вызывает метод get_absolute_url() по каждому объекту по умолчанию).
        """

        return Post.published.all()

    def lastmod(self, obj):
        """
        Извлекает каждый объект, возвращаемый методом items() и возвращает время
        последнего изменения объекта.
        """

        return obj.updated
