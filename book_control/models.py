from django.db import models
from user_control.models import PublisherProfileModel


class UniversityModel(models.Model):
    university = models.CharField(max_length=30)

    def __str__(self):
        return self.university


class DepartmentModel(models.Model):
    university = models.ForeignKey(UniversityModel, on_delete=models.CASCADE)
    department = models.CharField(max_length=200)

    def __str__(self):
        return self.department + " - " + self.university.university


class CourseModel(models.Model):
    university = models.ForeignKey(UniversityModel, on_delete=models.CASCADE)
    department = models.ForeignKey(DepartmentModel, on_delete=models.CASCADE)
    course = models.CharField(max_length=200)

    def __str__(self):
        return self.course + " - " + self.university.university


class BookModel(models.Model):
    name = models.CharField(max_length=200)
    university = models.ForeignKey(UniversityModel, on_delete=models.CASCADE)
    department = models.ForeignKey(DepartmentModel, on_delete=models.CASCADE)
    course = models.ForeignKey(CourseModel, on_delete=models.CASCADE)
    author = models.CharField(max_length=200)
    edition = models.CharField(max_length=200, null=True, blank=True)
    slug = models.SlugField(max_length=200)
    image = models.ImageField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    publisher = models.ForeignKey(PublisherProfileModel, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
