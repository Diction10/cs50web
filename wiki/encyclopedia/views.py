from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
import random
from .forms import *

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


# Title page view
def title_page(request, title):
    # get entry by its title
    content = util.get_entry(title)
    # display content on the web page
    if content != None:
        return render(request, "encyclopedia/title.html", {
            'title': title,
            "content": content    
        })
    return render(request, "encyclopedia/error.html", {
            'message': 'Sorry this page does not exist!!!'
    })


# search view function
def search(request):
    params = request.GET.get('q').lower()
    print('You searched for: ', params)

    # convert entries to lowercase
    entries = [entry.lower() for entry in util.list_entries()]

    if params in entries:
        return redirect('title_page', params)
    else:
        # create an empty list
        search = []

        # Get the length of the search parameter
        sub = params[:len(params)+1]

        # loop through the list of entries
        for entry in entries:
            # get the length of each list entries
            string = entry[:len(entry)+1]

            # check to see if the search parameter is a substring of any of the list entries
            if sub in string:
                # add entry to list
                search.append(entry)

                # display on the web page
                return render(request, "encyclopedia/index.html", {
                    "entries": search
                })
    
        return render(request, "encyclopedia/error.html", {
            'message': 'Sorry this page does not exist!!!'
        })


def new_page(request):
    # form = NewPageForm()
            
    if request.method == 'POST':
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            print('TITLE:', title)
            content = form.cleaned_data['content']

            # check if the title already exists
            if title not in util.list_entries():
                util.save_entry(title, content)
                # form.save()
                # redirect to the new page
                return redirect('title_page', title)

            return render(request, "encyclopedia/error.html", {
                'message': 'Sorry this title already exist!!!'
            })
    else:
        form = NewPageForm()

    return render (request, "encyclopedia/new_page.html", {
        'form': form
    })


def edit_page(request, title):
    content = util.get_entry(title)

    # To prepopulate the form
    form = EditPageForm(initial={'title': title, 'content':content})

    if request.method == 'POST':
        form = EditPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            
            content = form.cleaned_data['content']

            util.save_entry(title, content)

            # redirect to the new page
            return redirect('title_page', title)

    return render (request, "encyclopedia/edit_page.html", {
        'form': form,
        'title': title
    })
        


def random_page(request):
    # get an entry randomly
    random_entry = random.choice(util.list_entries())

    # Redirect to the page entry
    return redirect('title_page', random_entry)
 