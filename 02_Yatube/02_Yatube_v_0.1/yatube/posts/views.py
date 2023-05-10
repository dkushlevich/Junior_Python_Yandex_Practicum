from django.shortcuts import get_object_or_404, render

from yatube.settings import PAGE_VIEW_MULTIPLIER

from .models import Group, Post


def index(request):
    posts = Post.objects.select_related('group')[:PAGE_VIEW_MULTIPLIER]
    context = {'posts': posts}
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.select_related('group')[:PAGE_VIEW_MULTIPLIER]
    context = {'group': group, 'posts': posts}
    return render(request, 'posts/group_list.html', context)
