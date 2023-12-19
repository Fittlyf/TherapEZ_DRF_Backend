from django.db import models


class Exercise(models.Model):
    name = models.CharField(max_length=100)
    sets = models.IntegerField(default=2)
    description = models.TextField()
    image = models.ImageField(upload_to='exercise_images/', blank=True)
    cover_image = models.ImageField(upload_to='cover_exercise_images/', blank=True)
    link = models.URLField(blank=True)
    data = models.JSONField(default=dict, blank=True, null=True)
    time = models.PositiveIntegerField(default=45)
    coordinates_file = models.FileField(upload_to='exercise_coordinates/', blank=True, null=True)
    degree_of_strictness = models.IntegerField(default=75)
    matching_points_data = models.JSONField(default=dict({"points": []}))

    def __str__(self):
        return self.name
