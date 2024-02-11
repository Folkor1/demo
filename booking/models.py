from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


CHOICES = (
    ('Confirmed', 'Confirmed'),
    ('Pending', 'Pending'),
    ('Cancelled', 'Cancelled')
)

FINALIZED_CHOICES = (
    ('Not finalized', 'Not finalized'),
    ('Discarded', 'Discarded'),
    ('Finalized', 'Finalized')
)
        

class Bookings(models.Model):
    """
    Class for Bookings model
    """
    lesson = models.CharField(max_length=50)
    lesson_type = models.CharField(max_length=50)
    date = models.DateField()
    time = models.TimeField()
    status = models.BooleanField(default=False)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    confirmed = models.CharField(max_length=50, choices=CHOICES, default='Pending')
    datetime_booked = models.DateTimeField(default=timezone.now)
    finalized = models.CharField(max_length=50, choices=FINALIZED_CHOICES, default='Not finalized')
    notes = models.TextField(blank=True)
    comms = models.TextField(blank=True)
    flagged = models.BooleanField(blank=True, default=False)

    def get_lesson(self):
        """
        Return lesson name
        """
        return self.lesson

    def get_lesson_type(self):
        """
        Return lesson type name
        """
        return self.lesson_type

    def get_date(self):
        """
        Return date
        """
        return self.date

    def get_time(self):
        """
        Return time
        """
        return self.time

    def get_student(self):
        """
        Return student
        """
        return self.student
    
    def get_confirmed(self):
        """
        Return confirmed status
        """
        return self.confirmed
    
    def get_datetime_booked(self):
        """
        Return datetime_booked
        """
        return self.datetime_booked
    
    def get_finalized(self):
        """
        Return finalized
        """
        return self.finalized
    
    def get_notes(self):
        """
        Return notes
        """
        return self.notes
    
    def get_comms(self):
        """
        Return comments
        """
        return self.comms

    class Meta:
        ordering = ['-date']
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'
