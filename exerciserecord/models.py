from django.db import models
from django.utils import timezone
from patient.models import Patient
from exercise.models import Exercise
from patient_exercise.models import PatientExercise

class ExerciseRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='exercise_records')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='exercise_records')
    date = models.DateField()
    video = models.CharField(max_length=255, default='', null=True, blank=True)
    review = models.BooleanField(null=True, blank=True)
    commment = models.TextField(blank=True)
    blob = models.FileField(upload_to='exercise_records/', null=True, blank=True)

    def __str__(self):
        return f'{self.patient} - {self.exercise} - {self.date}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Call the parent class's save method to save the object

        # Calculate whether all exercises are completed for the patient on this date
        patient_exercises = PatientExercise.objects.filter(patient=self.patient)
        exercise_records = ExerciseRecord.objects.filter(date=self.date, patient=self.patient)

        # Get the set of exercise IDs for the patient's exercises and the recorded exercises
        patient_exercise_ids = set(patient_exercise.exercise.id for patient_exercise in patient_exercises)
        recorded_exercise_ids = set(exercise_record.exercise.id for exercise_record in exercise_records)

        # Check if all exercises are completed
        completed_all_exercises = patient_exercise_ids == recorded_exercise_ids

        # If all exercises are completed, update the patient's completed_exercise_date
        if completed_all_exercises:
            self.patient.completed_exercise_date = timezone.now()  # Update to the current date and time
            self.patient.save()