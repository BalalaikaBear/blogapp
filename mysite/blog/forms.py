from django import forms
from .models import Comment


class EmailPostForm(forms.Form):
    """Форма для отправки поста по электронной почте"""
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(
        required=False,
        widget=forms.Textarea
    )


class CommentForm(forms.ModelForm):
    """Форма для создания комментария. Форма создана на основе имеющейся модели Comment"""
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']  # заполняемые пользователем поля, для создания комментария


class SearchForm(forms.Form):
    """Форма для поискового запроса по нахождению постов"""
    query = forms.CharField()
