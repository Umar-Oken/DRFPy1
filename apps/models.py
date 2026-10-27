from django.conf import settings
from django.db import models
from django.db.models.fields.files import ImageField


# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=255, verbose_name="Sarlavha")
    is_done = models.BooleanField(db_default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    photo = ImageField(upload_to="%Y/%m/%d/" , blank=True , null=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tasks", null=True
    )
