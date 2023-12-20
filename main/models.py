from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User



# Create your models here.

class ExtraUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

class Follower(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")
    extrauser = models.ForeignKey(ExtraUser, on_delete=models.CASCADE, null=True)
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")

    class Meta:
        unique_together = ("user", "following")
    
    @staticmethod
    def get_followers_count(user):
        return Follower.objects.filter(user=user).count()
    
    @staticmethod
    def get_following_count(user):
        return Follower.objects.filter(following=user).count()
    
    @staticmethod
    def is_following(user1, user2):
        return Follower.objects.filter(user=user1, following=user2).exists()

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length = 100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    picture = models.ImageField(upload_to="post_photos/", blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        # Slugify the title
        self.slug = slugify(self.title[:40])

        # Check for uniqueness
        if Post.objects.filter(slug=self.slug).exists():
            # If a matching slug exists, generate a unique one
            counter = 1
            while Post.objects.filter(slug=self.slug).exists():
                self.slug = f"{slugify(self.title)}-{counter}"
                counter += 1

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return f'/posts/{self.slug}'

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    comment = models.TextField(max_length=600)
