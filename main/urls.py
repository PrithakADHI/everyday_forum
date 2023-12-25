from django.urls import path

from . import views

from django.conf import settings
from django.conf.urls.static import static

from django.views.generic.base import TemplateView


urlpatterns = [
    path("", views.index, name="index"),
    path("user_list", views.user_list, name="user_list"),
    path("user_posts/<str:username>", views.user_posts, name="user_posts"),
    path("following_list/<str:username>", views.following_list, name="following_list"),
    path("follower_list/<str:username>", views.follower_list, name="follower_list"),
    path("add_follower/<int:follower_id>", views.add_follower_ajax, name="add_follower_ajax"),
    path("delete_follower/<int:follower_id>", views.delete_follower_ajax, name="delete_follower_ajax"),
    path("add_follower_2/<int:follower_id>", views.add_follower, name='add_follower'),
    path("delete_follower_2/<int:follower_id>", views.delete_follower, name='delete_follower'),

    path('delete_comment/<int:comment_id>', views.delete_comment, name='delete_comment'),

    path("tests", views.tests, name="tests"),

    path("add_post", views.post_add, name="post_add"),
    path("delete_post/<int:pk>", views.delete_post, name="post_delete"),
    path("posts/<slug:post_slug>", views.post_details, name="post_details"),

    path("register", views.register_view, name="register"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),

    path("notifications", views.notifications, name='notification'),

    path("search_results", views.search_results, name='search_results'),
    path("search_button", views.search_button, name='search_button'),

    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)