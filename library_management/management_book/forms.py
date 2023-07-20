from django import forms

SEARCH_CHOICES = [
    ('title', 'Title'),
    ('author', 'Author'),
    ('genre', 'Genre'),
    ('isbn', 'ISBN'),
]

class BookSearchForm(forms.Form):
    search_option = forms.ChoiceField(label='Search By', choices=SEARCH_CHOICES)
    search_query = forms.CharField(label='Search Query')
    
    
    
from django import forms

class BookImportForm(forms.Form):
    csv_file = forms.FileField(label='Select CSV file')
