from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    access = models.BooleanField()


class Lesson(models.Model):
    products = models.ManyToManyField(Product)
    name = models.CharField(max_length=100)
    video_link = models.URLField()
    duration = models.DurationField()


class LessonView(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    viewed_time = models.DurationField()
    status = models.CharField(max_length=20, choices=[("Просмотрено", "просмотрено"),
                                                      ("Не просмотрено", "не просмотрено")])

    def save(self, *args, **kwargs):
        if (self.viewed_time / self.lesson.duration) >= 0.8:
            self.status = "Просмотрено"
        else:
            self.status = "Не просмотрено"
        super().save(*args, **kwargs)
