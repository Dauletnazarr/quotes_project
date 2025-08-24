from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import Source, Quote

class QuoteTests(TestCase):
    def setUp(self):
        self.s = Source.objects.create(name='The Matrix', type='movie')

    def test_no_duplicates(self):
        Quote.objects.create(source=self.s, text='There is no spoon', weight=1)
        q2 = Quote(source=self.s, text='  there  is   no SPOON ', weight=2)
        with self.assertRaises(ValidationError):
            q2.full_clean()

    def test_max_three_per_source(self):
        for i in range(3):
            Quote.objects.create(source=self.s, text=f'Q{i}', weight=1)
        q4 = Quote(source=self.s, text='Q3', weight=1)
        with self.assertRaises(ValidationError):
            q4.full_clean()
