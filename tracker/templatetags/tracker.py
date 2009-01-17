from django.template import Library
from simplebtt.tracker.forms import TorrentSearch

from simplebtt.tracker.models import Torrent, User, Client, Stat, Category# TorrentForm

register = Library()

@register.inclusion_tag('tracker/templatetags/search_form.html',takes_context=True)
def search_form( context):
    return {
            'form': TorrentSearch(),
            }

@register.inclusion_tag('tracker/templatetags/category.html',takes_context=True )
def category( context ):
    return {
            'count_all': Torrent.objects.all().count(),
            'category': Category.objects.all(),
            }

@register.inclusion_tag('tracker/templatetags/num_page.html',takes_context=True )
def num_page( context, num_page, step=20, category=None, ):
    page = num_page['page']
    step = num_page['step']
    category = num_page['category']
    count = num_page['count']

    if count <= step:
        next_page = False

    return {
            'prev_page': page-1,
            'next_page': next_page,
            'step':step,
            'category': category,
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
