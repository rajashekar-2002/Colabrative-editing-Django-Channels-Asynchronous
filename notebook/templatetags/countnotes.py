from django import template
register = template.Library() #decorator

from django.utils.safestring import mark_safe
from notes.models import Notes
from notebook.models import Notebook
from signin.models import User
from django.db.models import Q

import datetime

now = datetime.datetime.now()



@register.filter(name='count_notes')
def count_notes (notebook,email):
    # return Notebook.objects.filter(book_name=notebook).notes.count()
    return Notes.objects.filter(Q(notebook__notebook_slug=notebook) & Q(notebook__user__email=email)).count()

        
@register.filter(name='tagname')
def tagname (text,query):
    return mark_safe(text.replace(query,"<mark>"+query+"</mark>"))
    

@register.filter(name='share_book_error')
def share_book_error (request):
    request.session['error']=None
    return


@register.filter(name='neg_value')
def neg_value(value):

    return value*-1


@register.filter(name='abs_value')
def abs_value(value):
    try:
        return abs(value)
    except:
        return None
    


@register.filter(name='tag')
def tag(note,request):
    email=request.session.get('user')
    notebook=request.session.get('notebook')
    object=Notes.objects.filter( Q(notes_slug=note) & Q(notebook__user__email=email)).first()
    if object:
        text=object.tags
        text=text.split()
        return text
    else:
        return