from django.db import models

# Create your models here.


class Tag(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False)
    color = models.CharField(max_length=10)
    count = models.IntegerField(default=0)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
        indexes = [
            models.Index(
                fields=[
                    "id",
                ]
            ),
            models.Index(
                fields=[
                    "name",
                ]
            ),
        ]

    def __str__(self):
        return self.name