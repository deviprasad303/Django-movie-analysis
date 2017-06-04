from django import forms

from webapp.models import Post
from webapp.models import Post2


class PostForm(forms.ModelForm):

     class Meta:
         model = Post
         fields = ('title', 'text')


class PostForm2(forms.ModelForm):
    class Meta:
        model = Post2
        fields = ('name',)