from django.db import models
# from exercise.process_video import process_video_and_write_to_json
# import os

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
    video = models.FileField(upload_to='exercise_videos/', blank=True, null=True)

    # def save(self, *args, **kwargs):
    #     # Save the instance
    #     super().save(*args, **kwargs)

    #     # Process and save JSON if video is provided
    #     if self.video:
    #         video_path = self.video.path
    #         output_json = os.path.join('media/exercise_coordinates/', f'{self.name}_coordinates.json')
    #         output_path = os.path.join('exercise_coordinates/', f'{self.name}_coordinates.json')
    #         process_video_and_write_to_json(video_path, output_json)
    #         self.coordinates_file.name = output_path

    #         # Save the instance again with updated coordinates_file field
    #         super().save(*args, **kwargs)

    def __str__(self):
        return self.name
