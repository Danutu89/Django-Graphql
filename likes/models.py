from django.db import models

# Create your models here.


class Like(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False)
    icon = models.CharField(max_length=20)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Like"
        verbose_name_plural = "Likes"
        indexes = [
            models.Index(
                fields=[
                    "id",
                ]
            ),
        ]

    def __str__(self):
        return self.name