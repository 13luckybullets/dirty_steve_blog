from django.shortcuts import render, redirect
from .forms import *
from django.contrib import auth
from .models import *
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

from django.contrib.auth import views as auth_views
from django.template.context_processors import csrf
from django.contrib.auth.forms import AuthenticationForm


def articles(request):
    posts = Post.objects.all().order_by("-published_date")
    for post in posts:
        post.likes_counter = Like.objects.filter(post_id=post).count()
        post.comments_counter = Comment.objects.filter(post_id=post).count()

    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'articles.html', {'posts': posts,
                                             'username': auth.get_user(request).username})


def get_post(request, pk):
    post_content = Post.objects.get(id=pk)
    post_content.likes_counter = Like.objects.filter(post_id=pk).count()
    post_content.form = CommentForm
    post_content.comments = Comment.objects.filter(post=pk).order_by("date")
    return render(request, "post.html", {'content_post': post_content,
                                         'username': auth.get_user(request).username})


def add_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('get_post', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'post_form.html', {'form': form, "title": "Add new post",
                                             'username': auth.get_user(request).username})


def sign_up(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            user = auth.authenticate(username=form.cleaned_data['username'],
                                     password=form.cleaned_data['password2'])
            auth.login(request, user)
            return redirect('home')
    return render(request, "sign_up.html", {'form': form})


def add_like(request, post, user):
    page = request.META.get('HTTP_REFERER', '/')
    try:
        Like.objects.get(post_id=post, user_id=user).delete()
    except ObjectDoesNotExist:
        Like.objects.create(post_id=post, user_id=user).save()
    return redirect(page)


def edit_post(request, pk):
    post = Post.objects.get(id=pk)
    form = PostForm(initial={'title': post.title, 'text': post.text})
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post.title = form['title'].value()
            post.text = form['text'].value()
            post.save()
            return redirect('get_post', pk=post.pk)

    return render(request, 'post_form.html', {'form': form, "title": "Edit post",
                                              'username': auth.get_user(request).username})


def add_comment(request, pk):
    if request.POST:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = Post.objects.get(id=pk)
            comment.save()
    return redirect('get_post', pk)


def profile(request, pk):
    data = {}
    user = User.objects.get(id=pk)
    data['username'] = user.username
    data['email'] = user.email
    data['posts'] = Post.objects.filter(author_id=pk).count()
    data["comments"] = Comment.objects.filter(author_id=pk).count()

    like_counter = 0
    for i in Post.objects.filter(author_id=pk):
        like_counter += Like.objects.filter(post_id=i.id).count()
    data['like_counter'] = like_counter

    return render(request, 'view_profile.html', {'data': data,
                                                 'username': auth.get_user(request).username})


def edit_profile(request, pk):

    def change_email(request, pk):
        form = UpdateEmail(data=request.POST, instance=request.user)
        if form.is_valid():
            update = form.save(commit=False)
            update.user = User.objects.get(id=pk)
            update.save()

    def change_password(request, p_form):
        if p_form.is_valid():
            user = p_form.save()
            update_session_auth_hash(request, user)

    form = UpdateEmail(instance=request.user)
    p_form = PasswordChangeForm(request.user, request.POST)
    if request.method == 'POST':
        form = change_email(request, pk)
        p_form = change_password(request, p_form)
        return redirect('profile', pk)

    return render(request, 'edit_profile.html', {'form': form, "p_form": p_form,
                                                 'username': auth.get_user(request).username})



