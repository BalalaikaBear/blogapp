from django.urls import path
from . import views
from .feeds import LatestPostsFeed

app_name = 'blog'

urlpatterns = [
    # главная страница со списком постов
    path('', views.post_list, name='post_list'),
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
    #path('', views.PostListView.as_view(), name='post_list'),

    # пост
    path('<int:year>/<int:month>/<int:day>/<slug:post>', views.post_detail, name='post_detail'),

    # поиск постов по введенному запросу
    path('search/', views.post_search, name='post_search'),

    # отправка поста по электронной почте
    path('<int:post_id>/share/', views.post_share, name='post_share'),

    # добавление комментария к посту
    path('<int:post_id>/comment/', views.post_comment, name='post_comment'),

    # новостная RSS-лента
    path('feed/', LatestPostsFeed(), name='post_feed'),
]
