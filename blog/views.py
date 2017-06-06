# -*- coding: utf-8 -*-
from django.core.mail import send_mail
from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from taggit.models import Tag
from django.shortcuts import render_to_response
from blog.models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from blog.forms import EmailPostForm, ComentForm


def post_list(request, tag_slug=None):
    object_list = Post.publiched.all()

    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 3)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:

        posts = paginator.page(1)
    except EmptyPage:

        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/post/list.html', {'posts': posts, 'page': page, 'tag': tag})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             slug=post,
                             status='publiched',
                             publich__year=year,
                             publich__month=month,
                             publich__day=day)

    comments = post.comments.filter(active=True)

    if request.method == 'POST':

        comment_form = ComentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()

    else:
        comment_form = ComentForm()

    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.publiched.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publich')[:4]

    return render(request, 'blog/post/detail.html', {'post': post,
                                                     'comments': comments,
                                                     'comment_form': comment_form,
                                                     'similar_posts': similar_posts, })


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='publiched')
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) рекомендую к прочтению "{}"'.format(cd['name'], cd['email'], post.title)

            message = 'Читать "{}" at {}\n\n{}\'s комментарий: {}'.format(post.title, post_url, cd['name'],
                                                                          cd['comments'])

            send_mail(subject, message, 'pythontestsmail@gmail.com', [cd['to']])

            sent = True

    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent})

def search_form(request):
    return render_to_response('search_form.html')