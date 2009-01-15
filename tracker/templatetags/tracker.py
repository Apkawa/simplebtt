from django.template import Library
from simplebtt.tracker.forms import TorrentSearch

from simplebtt.tracker.models import Torrent, User, Client, Stat, Category# TorrentForm

register = Library()

@register.inclusion_tag('tracker/search_form.html',takes_context=True)
def search_form( context):
    return {
            'form': TorrentSearch(),
            }

@register.inclusion_tag('tracker/category.html',takes_context=True )
def category( context ):
    return {
            'count_all': Torrent.objects.all().count(),
            'category': Category.objects.all(),
            }
'''
@register.inclusion_tag('docs/search_form.html', takes_context=True)
def search_form(context, search_form_id='search'):
    request = context['request']
    auto_id = 'id_%s_%%s' % search_form_id
    return {
        'form': SearchForm(initial=request.GET, auto_id=auto_id),
        'search_form_id': search_form_id,
        'action': context['search'],
    }
    '''
