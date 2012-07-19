from django.db import models


class Presentation(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)

class Slide(models.Model):
    content = models.TextField()
    description = models.TextField(blank=True)
    presentation = models.ForeignKey(Presentation)
    id_title = models.CharField(max_length=20) #TODO walidacja o braku spacji itp
    created_at = models.DateTimeField()
    order_number = models.IntegerField()
    
    class Meta:
        unique_together = (("presentation","order_number"),)

class Position(models.Model):
    id = models.ForeignKey(Slide, primary_key=True)
    pos_x = models.IntegerField()
    pos_y = models.IntegerField()
    pos_z = models.IntegerField(blank=True)
    rotation = models.IntegerField(blank=True)