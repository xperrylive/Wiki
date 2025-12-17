from django.shortcuts import render,redirect
from . import util
from .forms import EntryForm
from markdown2 import markdown
from django.http import Http404
from random import choice

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def display_encyclopedia(request, title):
    entry = util.get_entry(title)
    if not entry:
        raise Http404()
    html_output = markdown(entry)
    return render(request, "encyclopedia/entry.html", {"title": title,"html_content": html_output})


# GET for search 
def search(request):
    query = request.GET.get("q","").strip().lower()
    if not query:
        return render(request, "encyclopedia/search_result.html", {"entries": []})
    entries = util.list_entries()
    match = []
    for entry in entries:
        entry_lower= entry.lower()
        if query == entry_lower:
            return redirect('entry', entry)
        
        if query in entry_lower:
            match.append(entry)
    
    return render(request, "encyclopedia/search_result.html", {"entries": match})

def create_entry(request):
    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            markdown_content = form.cleaned_data["markdown_content"]
            util.save_entry(title,markdown_content)
            return redirect("entry", title=title)
    else:
        form = EntryForm()
    
    return render(request,"encyclopedia/create_entry.html", {"form":form})

def edit_entry(request, title):
    if request.method == "POST":
        form = EntryForm(request.POST, original_title=title)
        if form.is_valid():
            new_title = form.cleaned_data["title"]
            markdown_content = form.cleaned_data["markdown_content"]
            util.save_entry(new_title, markdown_content)
            if new_title.lower().strip() != title.lower().strip(): 
                util.delete_entry(title)

            return redirect("entry", title=new_title)   
        else:
            return render(request, "encyclopedia/edit_entry.html", {"form":form})
    else:
        entry = util.get_entry(title)
        if not entry:
            raise Http404()
        initial_data = {"title": title, "markdown_content":entry.strip()}
        form = EntryForm(initial=initial_data)

    return render(request, "encyclopedia/edit_entry.html", {"form":form})


def random_entry(request):
    entries = util.list_entries()
    random_entry = choice(entries)
    return redirect("entry", title=random_entry)