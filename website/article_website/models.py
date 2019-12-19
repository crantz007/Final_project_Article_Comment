from django.db import models

# Create your models here.
from django.db import models
from tinymce import HTMLField
from django.core.urlresolvers import reverse




def validate_file_extension(value):
    import os
    from django.core.exceptions import ValidationError

    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['jpg', '.png', '.jpeg']
    if not ext.lower() in valid_extensions:
        raise ValidationError(u' Please select the required image format')

    class Category(models.Model):
        class Meta:
            verbose_name = 'Category'
            verbose_name_plural = 'Categories'

        title = models.CharField(primary_key=True, max_length=50, null=False, blank=False, verbose_name='Title')

        def __str__(self):
            return self.title.title()

    class Article(models.Model):
        class Meta:
            verbose_name_plural = "Articles"

        id = models.AutoField(primary_key=True)
        title = models.CharField(max_length=100, null=False, blank=False, verbose_name='Title')
        category = models.ForeignKey(Category, null=False, blank=False, verbose_name='Category')
        date = models.DateTimeField(auto_now_add=True)
        content = HTMLField(null=False, blank=False, verbose_name='Contents')
        summary = models.TextField(null=False, blank=False, verbose_name='Summary')
        image = models.FileField(validators=[validate_file_extension], blank=True, verbose_name='Image')

        def get_url(self):
            return reverse('articles:article', kwargs={'pk': self.id})

        def __str__(self):
            return self.title + "," + self.category.title

        class Comment(models.Model):
            class Meta:
                verbose_name = 'Comment'
                verbose_name_plural = 'Comments'

            id = models.AutoField(primary_key=True)
            article = models.ForeignKey(Article, null=False, blank=False, verbose_name='Article')
            visitor_name = models.CharField(max_length=50, null=False, blank=False, verbose_name="Visitor's name")
            visitor_email = models.EmailField(max_length=50, null=False, verbose_name="Visitor's Email")
            date = models.DateTimeField(auto_now_add=True)
            content = models.TextField(null=False, blank=False, verbose_name='Content')

            def __str__(self):
                return self.visitor_name + "," + self.content
