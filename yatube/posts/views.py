from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from .models import Post, Group, User

TEN = 10


def index(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, TEN)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    paginator = Paginator(group.posts.all(), TEN)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    posts = group.posts.all()[:TEN]
    context = {
        'group': group,
        'paginator': paginator,
        'page_number': page_number,
        'page_obj': page_obj,
        'posts': posts,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts = Post.objects.all()
    author_total_posts = Post.objects.filter(author_id=author.pk).__len__
    paginator = Paginator(author.posts.all(), 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'author': author,
        'paginator': paginator,
        'page_number': page_number,
        'page_obj': page_obj,
        'posts': posts,
        'author_total_posts': author_total_posts,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    posts = Post.objects.all()
    author_total_posts = Post.objects.filter(author_id=post.author.pk).__len__
    context = {
        'posts': posts,
        'post': post,
        'author_total_posts': author_total_posts,

    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    form = PostForm(request.POST or None)
    if not form.is_valid():
        return render(request, 'posts/create_post.html', {'form': form})
    post = form.save(commit=False)
    post.author = request.user
    post.save()
    return HttpResponseRedirect(reverse('posts:profile',
                                kwargs={'username': request.user}))


@login_required
def post_edit(request, post_id):
    is_edit = True
    post = get_object_or_404(Post, id=post_id)
    if post.author == request.user:
        form = PostForm(request.POST or None, instance=post)
        if form.is_valid():
            post = form.save()
            return HttpResponseRedirect(reverse('posts:post_detail',
                                        kwargs={'post_id': post_id}))
        form = PostForm(instance=post)
        return render(request, 'posts/create_post.html',
                      {'form': form, 'is_edit': is_edit, 'post': post})
    else:
        return HttpResponseRedirect(reverse('posts:profile',
                                    kwargs={'username': request.user}))
