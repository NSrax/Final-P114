from django import forms
from .models import Post, Author, Category

class PostForm(forms.ModelForm):
    author_name = forms.CharField(max_length=100, required=True)
    category_name = forms.CharField(max_length=100, required=True)

    class Meta:
        model = Post
        fields = ['title', 'content', 'author_name', 'category_name']

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['author_name'].initial = self.instance.author.name
            self.fields['category_name'].initial = self.instance.category.name

    def save(self, commit=True):
        author_name = self.cleaned_data['author_name']
        category_name = self.cleaned_data['category_name']

        author, created = Author.objects.get_or_create(name=author_name)
        category, created = Category.objects.get_or_create(name=category_name)

        post = super(PostForm, self).save(commit=False)
        post.author = author
        post.category = category

        if commit:
            post.save()
        return post
