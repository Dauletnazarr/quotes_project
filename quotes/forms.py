from django import forms
from .models import Quote

class QuoteForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = ('source', 'text', 'weight', 'is_active')

    def clean(self):
        cleaned = super().clean()
        self.instance.source = cleaned.get('source')
        self.instance.text = cleaned.get('text') or ''
        self.instance.weight = cleaned.get('weight') or 1
        self.instance.is_active = cleaned.get('is_active')
        self.instance.clean()
        return cleaned
