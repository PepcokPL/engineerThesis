"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from engineerThesis.presentation.models import Presentation, Slide


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

class SlideOrderNumberTests(TestCase):
    
    def setUp(self):
        "add presentation with no slides"
        self.presentation_with_no_slides = Presentation.objects.create(title="No slides", description="no description")
        
        self.presentation_with_one_slides = Presentation.objects.create(title="One slide", description="one")
        Slide.objects.create(content="first", description="first", order_number=1, presentation=self.presentation_with_one_slides)
    
        self.presentation_with_three_slides = Presentation.objects.create(title="Three slide", description="three")
        Slide.objects.create(content="firstOfThree", description="firstOfThree", order_number=1, presentation=self.presentation_with_three_slides)
        Slide.objects.create(content="secondOfThree", description="secondOfThree", order_number=2, presentation=self.presentation_with_three_slides)
        Slide.objects.create(content="thirdtOfThree", description="thirdOfThree", order_number=3, presentation=self.presentation_with_three_slides)
    
    def testOrderNumberWithNoSlides(self):
        
        max_slide_nb = self.presentation_with_no_slides.get_max_slide_order_number()
        expected_slide_nb = 1
        
        self.assertEqual(max_slide_nb, expected_slide_nb, "expected slide number is not 1")
        
    def testOrderNumberWithOneSlide(self):
        max_slide_nb = self.presentation_with_one_slides.get_max_slide_order_number()
        expected_slide_nb = 2
        
        self.assertEqual(max_slide_nb, expected_slide_nb, "expected slide number is not 2")
        
    def testOrderNumberWithThreeSlide(self):
        max_slide_nb = self.presentation_with_three_slides.get_max_slide_order_number()
        expected_slide_nb = 4
        
        self.assertEqual(max_slide_nb, expected_slide_nb, "expected slide number is not 4")