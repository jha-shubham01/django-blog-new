from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class CreateUpdateTimeStampModel(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(CreateUpdateTimeStampModel):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Tag(CreateUpdateTimeStampModel):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class StatusChoices(models.TextChoices):
    DRAFT = "Draft", _("Draft")
    PUBLISH = "Publish", _("Publish")
    ARCHIVE = "Archive", _("Archive")


class Post(CreateUpdateTimeStampModel):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(
        Category, related_name="posts", on_delete=models.SET_NULL, null=True, blank=True
    )
    image = models.ImageField(
        upload_to="post",
        default="post/sample.jpg",
    )
    status = models.CharField(
        max_length=10, choices=StatusChoices.choices, default=StatusChoices.DRAFT
    )
    tags = models.ManyToManyField(Tag, related_name="posts", blank=True)
    likes = models.ManyToManyField(User, related_name="liked_posts", blank=True)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()


class Comment(CreateUpdateTimeStampModel):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"
