# coding: utf-8

from django.db import models
from datetime import datetime

class Presentation(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    def __unicode__(self):
        return self.title
    
    def count_slides(self):
        return Slide.objects.filter(presentation_id = self.id).count()
    
    def get_add_slide_url(self):
        return '/' + str(self.id) + '/add_slide/'
    
    def get_edit_url(self):
        return '/presentation_edit/' + str(self.id) + '/'
    
    def get_delete_url(self):
        return '/presentation_delete/' + str(self.id) + '/' 
    
    def get_max_slide_order_number(self):
        presentation_slides = Slide.objects.filter(presentation=self)
        if not presentation_slides:
            return 1
        
        last_slide = presentation_slides.order_by('-order_number')[0]
        return last_slide.order_number + 1
    
    def delete(self, *args, **kwargs):
        "usuwamy slajdy"
        related_slides = Slide.objects.filter(presentation=self.id)
        print related_slides
        #super(Presentation,self).save(*args, **kwargs)
        
class Slide(models.Model):
    content = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    presentation = models.ForeignKey(Presentation)
    id_title = models.CharField(max_length=20, blank=True, null=True) #TODO walidacja o braku spacji itp
    created_at = models.DateTimeField(default=datetime.now())
    order_number = models.IntegerField() 
    # TODO dodac auto incerement
    
    def __unicode__(self):
        return "Presentation: " + str(self.presentation) + "; order nb: " + str(self.order_number)
    
    def get_url(self):
        return "/" + str(self.presentation.id) + '/slide_details/' + str(self.id)
    
    def get_edit_url(self):
        return "/" + str(self.presentation.id) + '/edit_slide/' + str(self.id)
    
    class Meta:
        unique_together = (("presentation","order_number"),)

class Position(models.Model):
    id = models.ForeignKey(Slide, primary_key=True)
    pos_x = models.IntegerField(blank=True, null=True)
    pos_y = models.IntegerField(blank=True, null=True)
    pos_z = models.IntegerField(blank=True, null=True)
    rotation = models.IntegerField(blank=True, null=True)
    
    def __unicode__(self):
        return "x:"+str(self.pos_x)+",y:"+str(self.pos_y)+",z:"+str(self.pos_z)