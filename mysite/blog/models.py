from django.conf import settings
from django.db import models
from django.utils import timezone

class Post(models.Model):
    # создание класса перечисления на основе Enum
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'  # Черновик
        PUBLISHED = 'PB', 'Published'  # Опубликован

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    author = models.ForeignKey(  # связь "многие к одному"
        settings.AUTH_USER_MODEL,  # AUTH_USER_MODEL по умолчанию указывает на auth.User
        on_delete=models.CASCADE,
        related_name='blog_posts'
    )
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.DRAFT
    )

    class Meta:
        # Сортировка, применяемая по умолчанию.
        # Индекс, повышает производительность запросов. Создается отдельный индекс в таблице.
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def __str__(self):
        return self.title
