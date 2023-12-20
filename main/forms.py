from django import forms
from django.db import IntegrityError
from .models import Post, ExtraUser, Comment

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