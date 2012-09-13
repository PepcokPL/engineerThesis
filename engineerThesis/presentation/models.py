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
    
    def get_details_url(self):
        return str(self.id) + '/details/'
    
    def get_delete_url(self):
        return '/presentation_delete/' + str(self.id) + '/' 
    
    def get_preview_url(self):
        return '/presentation_preview/' + str(self.id) + '/'
    
    def get_download_url(self):
        return '/presentation_download/' + str(self.id) + '/'  
    
    def get_max_slide_order_number(self):
        presentation_slides = Slide.objects.filter(presentation=self)
        if not presentation_slides:
            return 1
        
        last_slide = presentation_slides.order_by('-order_number')[0]
        return last_slide.order_number + 1
    
    def delete(self, *args, **kwargs):
        related_slides = Slide.objects.filter(presentation=self.id)
        if related_slides:
            for slide in related_slides:
                slide.delete_related_position()
                slide.delete()
        super(Presentation,self).delete(*args, **kwargs)
        
class Slide(models.Model):
    content = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    presentation = models.ForeignKey(Presentation)
    id_title = models.CharField(max_length=20, blank=True, null=True) #TODO walidacja o braku spacji itp
    created_at = models.DateTimeField(default=datetime.now())
    order_number = models.IntegerField() 
    # TODO dodac auto incerement
    #TODO napisac usuniecie slajdu
    
    def __unicode__(self):
        return "Presentation: " + str(self.presentation) + "; order nb: " + str(self.order_number)
    
    def get_url(self):
        return "/" + str(self.presentation.id) + '/slide_details/' + str(self.id)
    
    def get_edit_url(self):
        return "/" + str(self.presentation.id) + '/edit_slide/' + str(self.id)
    
    def get_delete_url(self):
        return "/" + str(self.presentation.id) + '/delete_slide/' + str(self.id)
    
    def get_preview_url(self):
        return "/" + str(self.presentation.id) + '/preview_slide/' + str(self.id)
    
    def has_id_title(self):
        if self.id_title != '':
            return True
        return False
    
    def delete_related_position(self):
        try:
            related_position = Position.objects.get(pk=self.id)
            related_position.delete()
        except Position.DoesNotExist:
            print "Pozycja slajdu" + self + "Nie isntieje"
            print 
            
    def decrement_order_number(self):
        self.order_number = self.order_number-1
        self.save()        
    
    @staticmethod
    def repair_slide_order(presentation_id, removed_order_number):
        slides_to_repair = Slide.objects.filter(presentation_id=presentation_id).filter(order_number__gt=removed_order_number)
        for slide in slides_to_repair:
            slide.decrement_order_number()
    
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
    
    def has_scale(self):
        if self.pos_z != '':
            return True
        return False
        
    def has_rotation(self):
        if self.rotation != '':
            return True
        return False