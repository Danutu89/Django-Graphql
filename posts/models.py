from django.db import models
from django.template.defaultfilters import slugify

# Create your models here.
class Post(models.Model):

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200, null=False)
    slug = models.SlugField(max_length=240)
    body = models.TextField()

    author = models.ForeignKey("users.user", on_delete=models.CASCADE)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    likes = models.ManyToManyField(
        "likes.like", through="posts.like", blank=True
    )
    likes_count = models.IntegerField(default=0)

    tags = models.ManyToManyField("tags.tag", blank=True)
    tags_count = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        indexes = [
            models.Index(fields=["id"]),
            models.Index(fields=["title"]),
        ]

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)

        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Like(models.Model):

    id = models.AutoField(primary_key=True)
    author = models.ForeignKey("users.user", on_delete=models.CASCADE)
    type = models.ForeignKey("likes.like", on_delete=models.CASCADE)
    post = models.ForeignKey("posts.post", on_delete=models.CASCADE)

    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Like"
        verbose_name_plural = "Likes"

    def __str__(self):
        return f"{self.type.name} {self.author.username}"
