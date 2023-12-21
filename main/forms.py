from django import forms
from django.db import IntegrityError
from django.contrib.auth.models import User
from .models import Post, ExtraUser, Comment
from django.contrib.auth.forms import UserCreationForm

class MakePost(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'picture']

    def clean_title(self):
        title = self.cleaned_data['title']
        try:
            Post.objects.get(title=title)
            raise forms.ValidationError("Title must be unique.")
        except Post.DoesNotExist:
            return title

class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = ExtraUser
        fields = ['profile_picture']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
    
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['comment'].widget.attrs.update({ 'class': 'comment', 'id': 'expandingTextarea', 'oninput': 'resizeTextarea()' })
    
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User  # Assuming ExtraUser is your user model
        fields = UserCreationForm.Meta.fields

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set placeholders for fields
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
