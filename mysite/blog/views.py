from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from .models import Post
from .forms import EmailPostForm, CommentForm


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 2
    template_name = 'blog/post/list.html'


def post_list(request: HttpRequest) -> HttpResponse:
    post_list = Post.published.all()

    # Постраничная разбивка с 2 постами на страницу
    paginator = Paginator(post_list, 2)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # если page_number не целое число -> выдать первую страницу
        posts = paginator.page(1)
    except EmptyPage:
        # если page_number находится вне диапазона -> выдать последнюю страницу
        posts = paginator.page(paginator.num_pages)

    return render(
        request,
        'blog/post/list.html',
        {'posts': posts}
    )


def post_detail(request: HttpRequest,
                year: int,
                month: int,
                day: int,
                post: str) -> HttpResponse:
    # вариант 1
    # try:
    #    post = Post.published.get(id=id)
    # except Post.DoesNotExist:
    #    raise Http404("No Post found.")

    # вариант 2
    post = get_object_or_404(Post, status=Post.Status.PUBLISHED,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day,
                             slug=post)

    # Список активных комментариев к этому посту
    comments = post.comments.filter(active=True)
    # Форма для комментирования пользователями
    form = CommentForm()

    return render(
        request,
        'blog/post/detail.html',
        {
            'post': post,
            'comments': comments,
            'form': form,
        }
    )


def post_share(request: HttpRequest, post_id: int) -> HttpResponse:
    # Извлечь пост по идентификатору id
    post = get_object_or_404(Post, status=Post.Status.PUBLISHED,
                             id=post_id)

    sent = False

    if request.method == 'POST':
        # Форма была передана на обработку
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Поля формы успешно прошли валидацию
            cd: dict = form.cleaned_data
            # Формирование полного URL-адреса, включая HTTP-схему и хост-имя (hostname)
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = (f"Read {post.title} at {post_url}\n\n"
                       f"{cd['name']}\'s comments: {cd['comments']}")
            send_mail(subject, message, 'your_account@gmail.com', [cd['to']])
            sent = True

    else:
        form = EmailPostForm()

    return render(
        request,
        'blog/post/share.html',
        {
            'post': post,
            'form': form,
            'sent': sent,
        }
    )


@require_POST  # при обращении другим методом выдает ошибку HTTP 405 (Метод не разрешен)
def post_comment(request: HttpRequest, post_id: int) -> HttpResponse:
    post = get_object_or_404(Post, status=Post.Status.PUBLISHED,
                             id=post_id)

    comment = None

    # Комментарий был отправлен
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # Создать объект класса Comment, не сохраняя его в базе данных
        comment = form.save(commit=False)
        # Назначить пост комментарию
        comment.post = post
        # Сохранить комментарий в базе данных
        comment.save()

    return render(
        request,
        'blog/post/comment.html',
        {
            'post': post,
            'form': form,
            'comment': comment,
        }
    )
