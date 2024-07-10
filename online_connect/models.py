from django.db import models

from accounts.models import User

# Create your models here.
class Appointment(models.Model):
    patient = models.ForeignKey(User,related_name="doctor_appointments",on_delete=models.CASCADE)
    doctor = models.ForeignKey(User,related_name="appointments",on_delete=models.CASCADE)
    required_speciality = models.CharField(max_length=250)
    date = models.DateField()
    time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('date',)
    def __str__(self):
        return f'{self.patient.first_name} - {self.doctor.first_name}'
    #     unique_together = ['patient','doctor']