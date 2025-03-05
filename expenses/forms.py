from django import forms
from .models import Expense
from datetime import date

class ExpenseForm(forms.ModelForm):
    
    class Meta:
        model = Expense
        fields = ['title', 'amount', 'category', 'date']

    def clean_date(self):
        selected_date = self.cleaned_data.get('date')
        if selected_date and selected_date > date.today():
            raise forms.ValidationError("The date cannot be in the future.")
        return selected_date
