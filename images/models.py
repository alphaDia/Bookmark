from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class Image(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="images_created",
        on_delete=models.CASCADE,
    )
    users_like = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="images_liked",
        blank=True,
    )
    title = models.CharField(_("Title"), max_length=200)
    slug = models.SlugField(_("Slug"), blank=True)
    url = models.URLField(_("Url"), max_length=2000)
    image = models.ImageField(_("Image"), upload_to="images/%Y/%m%d")
    description = models.TextField(_("Description"), blank=True)
    created = models.DateTimeField(_("Created"), auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["-created"]),
        ]
        ordering = [
            "-created",
        ]

    def get_absolute_url(self):
        return reverse("images:detail", args=[self.pk, self.slug])

    def __str__(self):
        return self.title

    def user_total_likes(self):
        return self.users_like.count()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)  # Call the real save() method
