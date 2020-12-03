from django.db import models

# Create your models here.

class FCI_regional_office(models.Model):
    office_name = models.CharField(max_length=200)
    office_Lat = models.FloatField(default=0)
    office_Long = models.FloatField(default=0)
    office_number = models.IntegerField(default=0)

    def __str__(self):
        return self.office_name
    class Meta:
        verbose_name_plural = 'FCI_regional_offices'

class godowns(models.Model):
    godowns_name = models.CharField(max_length=200)
    godowns_Lat = models.FloatField(default=0)
    godowns_Long = models.FloatField(default=0)
    godowns_number = models.IntegerField(default=0)

    def __str__(self):
        return self.godowns_name
    class Meta:
        verbose_name_plural = 'Godowns'
