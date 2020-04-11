from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
from .models import Post
from .forms import CreatePost


# Create your views here.
def forum(request):

    forum_posts = Post.objects.order_by('-date_posted')

    # Paginator
    paginator = Paginator(forum_posts, 6)
    page = request.GET.get('page')
    paged_posts = paginator.get_page(page)

    """Render Forum page and return all available posts with pagination and
    search functionality."""
    context = {
        'forum_page': 'active',
        'posts': paged_posts
    }

    return render(request, 'forum/forum.html', context)


def create_post(request):

    """Render Create Post and Create Post for display to the Forum"""
    if request.method == 'POST':
        # Get form values
        create_post_form = Post.objects.create(
            title=request.POST.get('title'),
            post_text=request.POST.get('post_text'),
            category=request.POST.get('category'),
            originator=request.user
        )

        create_post_form.save()
        messages.success(request, 'Post added to the Forum!')
        return redirect('forum-posts')

    context = {
        'form': CreatePost
    }

    return render(request, 'forum/create-post.html', context)


def view_post(request):
    """Create Forum Post."""
    return render(request, 'forum/view-post.html')
