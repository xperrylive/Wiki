from django import forms
from .util import list_entries

class EntryForm(forms.Form):
    title = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={"class":"form-control"}))
    markdown_content = forms.CharField(max_length=3000, required=True, widget=forms.Textarea(attrs={"class":"form-control"}))

    # Overrides __init__ to accept (original_title)
    # for the purpose of allowing to update the entry and keeping the same title 
    def __init__(self, *args, **kwargs):
        self.original_title = kwargs.pop("original_title",None)
        super().__init__(*args, **kwargs)

    def clean_title(self):
        title = self.cleaned_data["title"]
        entries =list_entries()

        # Make sure title is unique
        # Also ignore if it matches the title we are currently editing
        if title.lower().strip() in [e.lower().strip() for e in entries]:
            if self.original_title and title.lower().strip() == self.original_title.lower().strip():
                return title
        
            raise forms.ValidationError("An entry with this title already exists.")
        
        return title
    

    # removing extra whitespace when editing the form
    def clean_markdown_content(self):
        markdown_content = self.cleaned_data["markdown_content"]

        markdown_content = markdown_content.replace("\r\n", "\n")
        markdown_content = markdown_content.replace("\r", "\n")

        return markdown_content