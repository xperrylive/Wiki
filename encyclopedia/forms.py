from django import forms

class CreateEntry(forms.Form):
    title = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={"class":"form-control"}))
    markdown_content = forms.CharField(max_length=3000, required=True, widget=forms.Textarea(attrs={"class":"form-control"}))
    
