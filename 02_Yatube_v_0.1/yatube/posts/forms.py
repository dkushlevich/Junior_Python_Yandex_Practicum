from django import forms
from django.views.generic import UpdateView

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group')


class EditPostForm(UpdateView):
    model = Post
    template_name = 'posts/create_post.html'
    fields = ('text', 'group')
