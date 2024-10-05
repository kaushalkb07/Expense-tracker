from django import forms
from expenseapp.models import Expense

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['title', 'amount', 'category', 'slug', 'description', 'date']
        # Customizing widgets for specific input types
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control', 'id':'inputtitle', 'name':'title'}),
            'amount': forms.NumberInput(attrs={'class':'form-control', 'id':'inputAmount', 'name':'amount'}),
            'category': forms.Select(attrs={'class':'form-control', 'id':'inputCategory', 'name':'category'}),
            'slug': forms.TextInput(attrs={'class':'form-control', 'id':'inputSlug', 'name':'slug'}),
            'description': forms.Textarea(attrs={'class':'form-control', 'id':'description', 'name':'description'}),
            'date': forms.DateInput(attrs={'class':'form-control', 'id':'inputDate', 'name':'date', 'type': 'date'}),
        }