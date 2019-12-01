from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation

from django.db import models

from ckeditor_uploader.fields import RichTextUploadingField


# Create your models here.
# 博客分类模型
from read_stastic.models import ReadNumExpandMethod, ReadDetail


class BlogType(models.Model):
    type_name = models.CharField(max_length=15)

    def __str__(self):
        return self.type_name


class Blog(models.Model, ReadNumExpandMethod):
    title = models.CharField(max_length=50)
    blog_type = models.ForeignKey(BlogType, on_delete=models.CASCADE)
    content = RichTextUploadingField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    read_details=GenericRelation(ReadDetail)
    created_time = models.DateTimeField(auto_now_add=True)
    lastupdate_time = models.DateTimeField(auto_now=True)
    top=models.BooleanField(default=False)

    def __str__(self):
        return "<Blog:%s>" % self.title

    class Meta:
        ordering = ['-created_time']
