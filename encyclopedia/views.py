from django.shortcuts import render,redirect
from . import util
from .forms import EntryFrom
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
    search_query = request.GET.get("q","").strip().lower()
    if not search_query:
        return render(request, "encyclopedia/search_result.html", {"entries": []})
    # should retreive a list of encyclopedias not the whole file content
    entries = util.list_entries()
    for entry in entries:
        if search_query == entry.lower():
            return redirect('entry', entry)
    
    search_result = [entry for entry in entries if search_query in entry.lower() ]
    return render(request, "encyclopedia/search_result.html", {"entries": search_result})

def create_entry(request):
    if request.method == "POST":
        form = EntryFrom(request.POST)
        entries = util.list_entries()
        if form.is_valid():
            title = form.cleaned_data["title"]
            markdown_content = form.cleaned_data["markdown_content"]
            if title.lower().strip() not in [entry.lower().strip() for entry in entries]:
                util.save_entry(title,markdown_content)
                return redirect("entry", title=title)
            else:
                form.add_error('title', 'An entry with this title already exists.')
                return render(request,"encyclopedia/create_entry.html", {"form":form})
    else:
        form = EntryFrom()
    
    return render(request,"encyclopedia/create_entry.html", {"form":form})

def edit_encyclopedia(request, title):
    if request.method == "POST":
        form = EntryFrom(request.POST)
        if form.is_valid():
            new_title = form.cleaned_data["title"]
            markdown_content = form.cleaned_data["markdown_content"]
            entries = util.list_entries()
            if new_title.strip().lower() != title.strip().lower() and new_title.strip().lower() in [entry.strip().lower() for entry in entries]:
                form.add_error('title', 'An entry with this title already exists.')
                return render(request, "encyclopedia/edit_entry.html", {"form":form})
            util.save_entry(new_title, markdown_content)
            util.delete_entry(title) if new_title.strip().lower() != title.strip().lower() else None
            return redirect("entry", title=new_title)   
        else:
            return render(request, "encyclopedia/edit_entry.html", {"form":form})
    else:
        entry = util.get_entry(title)
        if not entry:
            raise Http404()
        initial_data = {"title": title, "markdown_content":entry}
        form = EntryFrom(initial=initial_data)

    return render(request, "encyclopedia/edit_entry.html", {"form":form})


def random_encyclopedia(request):
    entries = util.list_entries()
    random_entry = choice(entries)
    return redirect("entry", title=random_entry)