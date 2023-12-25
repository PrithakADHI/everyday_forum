from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import User, Follower, Post, ExtraUser, Comment, Notification

from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm

from .forms import MakePost, ProfilePictureForm, CommentForm, UserSearchForm

from datetime import datetime

# Create your views here.
def index(request):
    posts = Post.objects.all()
    if request.user.is_authenticated:
        following_users = Follower.objects.filter(user=request.user)
        followed_users = Follower.objects.filter(user=request.user).values_list('following', flat=True)
        profile_picture = ExtraUser.objects.get(user=request.user)

        if followed_users:
            random_posts = Post.objects.filter(user__in=followed_users).order_by("?")[:15]
        else:
            random_posts = []

        latest_post = Post.objects.filter(user=request.user).order_by('-created_at').first()

        if request.method == "POST":
            form = MakePost(request.POST, request.FILES)
            if form.is_valid():
                form_title = form.cleaned_data["title"]
                form_content = form.cleaned_data["content"]
                current_user = request.user
                current_time = datetime.now()
                if 'picture' in request.FILES:
                    Post(user=current_user, created_at=current_time, title=form_title, content=form_content, picture=request.FILES['picture']).save()
                else:
                    Post(user=current_user, created_at=current_time, title=form_title, content=form_content, picture=None).save()
                return redirect('index')
        else:
            form = MakePost()
        
    else:
        return redirect('login')
        

    return render(request, 'index.html', {'posts': posts, 'followings': following_users, 'user_profile': profile_picture, 'random_posts': random_posts, 'form': form, 'latest_post': latest_post})

def tests(request):
    return render(request, 'tests.html')


# For the Follower System

def user_list(request):
    current_user = request.user
    users = User.objects.all().exclude(id=current_user.id)
    followers = Follower.objects.filter(user=current_user)
    following_users = followers.values_list('following', flat=True)

    user_data = []
    for user in users:
        is_following = user.id in following_users
        user_data.append({'user': user, 'is_following': is_following})

    return render(request, 'user_list.html', {'user_data': user_data})
def following_list(request, username):
    current_user = User.objects.get(username=username)
    following = Follower.objects.filter(user=current_user)
    return render(request, 'following_list.html', {'followers': following, 'current_user': current_user})

def follower_list(request, username):
    current_user = User.objects.get(username=username)
    followers = Follower.objects.filter(following=current_user)
    return render(request, 'follower_list.html', {'followers': followers, 'current_user': current_user})

def add_follower(request, follower_id):
    if request.method == 'GET':
        follower = User.objects.get(id=follower_id)
        extra = ExtraUser.objects.get(user=request.user)
        Follower.objects.create(user=request.user, extrauser=extra, following=follower)
    return redirect(request.META.get('HTTP_REFERER', '/default-url/'))

def delete_follower(request, follower_id):
    if request.method == 'GET':
        follower = User.objects.get(id=follower_id)
        Follower.objects.filter(user=request.user, following=follower).delete()
    return redirect(request.META.get('HTTP_REFERER', '/default-url/'))

def add_follower_ajax(request, follower_id):
    if request.method == 'GET':
        follower = User.objects.get(id=follower_id)
        extra = ExtraUser.objects.get(user=request.user)
        Follower.objects.create(user=request.user, extrauser=extra, following=follower)

        followers_count = Follower.get_followers_count(follower)
        following_count = Follower.get_following_count(follower)

        notification_user = follower
        notification_sender_user = request.user
        notification_content = f"{ request.user.username } has followed you."

        Notification.objects.create(user=notification_user, content=notification_content, sender_user=notification_sender_user)

        Notification.objects.filter(user=follower).update(is_read=True)

        # Return a JSON response indicating success
        return JsonResponse({'status': 'success', 'followerCount': followers_count, 'followingCount': following_count})
    return JsonResponse({'status': 'error'})

def delete_follower_ajax(request, follower_id):
    if request.method == 'GET':
        follower = User.objects.get(id=follower_id)
        Follower.objects.filter(user=request.user, following=follower).delete()

        followers_count = Follower.get_followers_count(follower)
        following_count = Follower.get_following_count(follower)

        # Return a JSON response indicating success
        return JsonResponse({'status': 'success', 'followerCount': followers_count, 'followingCount': following_count})
    return JsonResponse({'status': 'error'})

def delete_comment(request, comment_id):
    if request.method == 'GET':
        comment = Comment.objects.get(id=comment_id)
        Comment.objects.filter(id=comment_id).delete()

        return redirect(request.META.get('HTTP_REFERER', '/default-url/'))

# For Posts
def user_posts(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(user=user)

    followers_count = Follower.get_followers_count(user)
    following_count = Follower.get_following_count(user)

    is_following = Follower.is_following(request.user, user)

    following = Follower.objects.filter(user=user)
    followers = Follower.objects.filter(following=user)

    context = {
        'user': user,
        'posts': posts,
        'followers_count': followers_count,
        'following_count': following_count,
        'is_following': is_following,
        'following': following,
        'followers': followers,
    }

    return render(request, 'user_posts.html', context)

def post_details(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    comments = Comment.objects.filter(post=post)

    default_comment = ''

    form = CommentForm(request.POST)
    if form.is_valid():
        form_comment = form.cleaned_data["comment"]
        Comment(user=request.user, post=post, comment=form_comment).save()

        notification_user = post.user
        notification_sender_user = request.user
        notification_post = post
        notification_content = f"{request.user} commented on your post"

        Notification.objects.filter(user=post.user).update(is_read=True)

        Notification.objects.create(user=notification_user, post=notification_post, sender_user=notification_sender_user, content=notification_content)

        return redirect('post_details', post_slug=post.slug)
    else:
        form = CommentForm(initial={'comment': default_comment})

    return render(request, 'post_details.html', {'post': post, 'comments': comments, 'form': form})

def post_add(request):
    if request.method == "POST":
        form = MakePost(request.POST, request.FILES)
        if form.is_valid():
            form_title = form.cleaned_data["title"]
            form_content = form.cleaned_data["content"]
            current_user = request.user
            current_time = datetime.now()
            if 'picture' in request.FILES:
                Post(user=current_user, created_at=current_time, title=form_title, content=form_content, picture=request.FILES['picture']).save()
            else:
                Post(user=current_user, created_at=current_time, title=form_title, content=form_content, picture=None).save()
            return redirect('index')
    else:
        form = MakePost()
        
    return render(request, 'post_add.html', {'form': form})

def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('index')

    return render(request, 'delete_post.html', {'post': post})

# For Authentication

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
            # Redirect to a success page.
        else:
            messages.error(request, 'Invalid login credentials. Please try again.')
            # Return an 'invalid login' error message.
    return render(request, 'login.html')

# Implement similar views for logout and registration.
def logout_view(request):
    logout(request)
    return redirect('index')

from django.contrib import messages

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        profile_form = ProfilePictureForm(request.POST, request.FILES)
        if form.is_valid() and profile_form.is_valid():
            user = form.save()

            if 'profile_picture' in request.FILES:
                profile = ExtraUser(user=user, profile_picture=request.FILES['profile_picture'])
                profile.save()
            else:
                profile = ExtraUser(user=user, profile_picture=None)
                profile.save()

            # Log the user in after registration, if needed.
            # Redirect to a success page or any desired URL after successful registration.
            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('login')  # Assuming 'login' is the name of your login URL.
        else:
            # Add error messages to the context
            error_messages = []
            error_messages.extend(form.errors.values())
            error_messages.extend(profile_form.errors.values())
            for message in error_messages:
                messages.error(request, message)

    else:
        form = UserCreationForm()
        profile_form = ProfilePictureForm()

    return render(request, 'register.html', {'form': form, 'profile_form': profile_form})

# For the Notification System

def notifications(request):
    notifications = Notification.objects.filter(user=request.user)

    Notification.objects.filter(user=request.user).update(is_read=False)

    return render(request, 'notifications.html', {'notifications': notifications})

# For the Searching System

def search_results(request):
    query = request.GET.get('query', '')
    results = User.objects.filter(username__icontains=query)
    return render(request, 'search_results.html', {'results': results, 'query': query})

def search_button(request):
    return render(request, 'search_button.html')