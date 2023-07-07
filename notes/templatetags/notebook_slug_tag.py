from django import template
register = template.Library() #decorator
from django.db.models import Q
from notes.models import Notes
from notebook.models import Notebook
from notes.models import Notes


        
@register.filter(name='notetext')
def notetext():
    return Notes.get_notetext()


@register.filter(name='session_list')
def session_list(tag,note):
    keys=tag.keys()
    for i in keys:
        if i==note:
            return tag.get(i)


@register.filter(name='tags')
def tags(note,request):
    email=request.session.get('user')
    notebook=request.session.get('notebook')
    object=Notes.objects.filter(Q(notebook__notebook_slug=notebook) & Q(notes_slug=note) & Q(notebook__user__email=email)).first()
    if object:
        text=object.tags
        text=text.split()
        return text
    else:
        return