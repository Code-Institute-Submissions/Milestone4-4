from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .models import Post, PostComment, categories
from .forms import CreatePost, CreateComment


# Function Views
def forum(request):
    """Render Forum page and return all available posts with pagination and
    filter functionality. Filter option generated via 'categories' list in
    models.py file."""
    forum_posts = Post.objects.order_by('-date_posted')

    # Paginator
    paginator = Paginator(forum_posts, 6)
    page = request.GET.get('page')
    paged_posts = paginator.get_page(page)

    context = {
        'forum_page': 'active',
        'categories': categories,
        'posts': paged_posts
    }

    return render(request, 'forum/forum.html', context)


def filter_posts(request):
    """Display categorised results based on Filter selection by User on
    Forum page. If user does not select viable category option, error message
    shown and redirected back to forum page with detail."""
    queryset_list = Post.objects.order_by('-date_posted')

    if 'category' in request.GET:
        category = request.GET['category']
        if category == '':
            messages.error(request, 'Please select Post Category before '
                                    'filtering!')
            return redirect('forum-posts')
        queryset_list = queryset_list.filter(category__iexact=category)

    context = {
        'posts': queryset_list
    }

    return render(request, 'forum/filtered-posts.html', context)


def view_post(request, post_id):
    """View Forum Post and render Comment Form & add comments to thread."""
    post = get_object_or_404(Post, pk=post_id)
    post_comments = PostComment.objects.filter(post_id=post_id).order_by(
        '-date_commented')

    if request.method == 'POST':
        create_comment_form = PostComment(
            comment_text=request.POST.get('comment_text'),
            commenter=request.user,
            post=post
        )
        create_comment_form.save()
        messages.success(request, 'Comment added to Post')
        return redirect('view-post', post_id)

    context = {
        'post': post,
        'comments': post_comments,
        'form': CreateComment
    }

    return render(request, 'forum/view-post.html', context)


def create_post(request):
    """Render create-post template and CreatePost form. Once form is filled
    out, save and display to the Forum."""
    if request.method == 'POST':
        # Get form values
        create_post_form = Post(
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


def edit_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        # Get form values
        edit_form = CreatePost(request.POST, instance=post)
        if edit_form.is_valid():
            edit_form.save()
            messages.success(request, 'Post updated!')
            return redirect('view-post', post_id)

    edit_form = CreatePost(instance=post)

    context = {
        'form': edit_form
    }

    return render(request, 'forum/edit-post.html', context)
