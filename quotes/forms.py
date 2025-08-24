from django import forms
from .models import Quote

class QuoteForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = ('source', 'text', 'weight', 'is_active')

    # Можно вообще без clean(), либо лёгкая нормализация текста:
    def clean_text(self):
        txt = (self.cleaned_data.get('text') or '').strip()
        return txt
