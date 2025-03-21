from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from PIL import Image as PILImage
import os


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Image(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images/')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name='images', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    categories = models.ManyToManyField(Category, blank=True, related_name='images')
    low_quality_image = models.ImageField(upload_to='images/low_quality/', blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image and not self.low_quality_image:
            image_path = self.image.path
            img = PILImage.open(image_path)
            img = img.convert("RGB")
            img.thumbnail((300, 300))

            low_quality_path = os.path.join(os.path.dirname(image_path), "low_quality_" + os.path.basename(image_path))
            img.save(low_quality_path, "JPEG", quality=60)

            self.low_quality_image.name = "images/low_quality/" + os.path.basename(low_quality_path)
            super().save(update_fields=['low_quality_image'])

    def __str__(self):
        return self.title


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    images = models.ManyToManyField(Image, blank=True)

    def __str__(self):
        return f"Cart of {self.user.username}"


class Like(models.Model):
    image = models.ForeignKey(Image, related_name='likes', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    image = models.ForeignKey(Image, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.image.title}"









class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
