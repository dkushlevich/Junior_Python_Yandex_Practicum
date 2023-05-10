from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from yatube.settings import PAGE_VIEW_MULTIPLIER

from .forms import PostForm
from .models import Group, Post, User
from .utils import paginator_for_posts


def index(request):
    posts = Post.objects.select_related('group')
    page_obj = paginator_for_posts(request, posts, PAGE_VIEW_MULTIPLIER)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.select_related('group')
    page_obj = paginator_for_posts(request, posts, PAGE_VIEW_MULTIPLIER)
    context = {'group': group, 'page_obj': page_obj}
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = user.posts.select_related('author')
    count_posts = user.posts.count()

    page_obj = paginator_for_posts(request, posts, PAGE_VIEW_MULTIPLIER)

    context = {'author': user,
               'page_obj': page_obj,
               'count_posts': count_posts,
               }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    count_posts = Post.objects.select_related(
        'author').filter(author=post.author).count()
    context = {'post': post, 'count_posts': count_posts}
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    author = Post(author=request.user)
    form = PostForm(request.POST or None, instance=author)
    if form.is_valid():
        form.save()
        return redirect('posts:profile', username=request.user)
    return render(request, 'posts/create_post.html', {'form': form})


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user != post.author:
        return redirect('posts:post_detail', post_id=post_id)
    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post_id=post_id)
    context = {'form': form, 'is_edit': True, 'post': post}
    return render(request, 'posts/create_post.html', context)
