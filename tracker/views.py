from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.utils.encoding import DjangoUnicodeDecodeError
from django.shortcuts import render_to_response
from django.conf import settings

from simplebtt.recaptcha import captcha
from simplebtt.tracker.models import Torrent, User, Client, Stat, Category# TorrentForm
from simplebtt.tracker.forms import TorrentAddForm

from urllib import unquote
from re import findall

def search( request ):
    if request.method == 'GET':
        if request.GET.get('search'):
            import re
            query = request.GET['search']
            regex = '!|'.join(re.sub('([\s]+|\n+)',' ', query).split(' '))
            finder = Torrent.objects.filter( name__iregex = r'(%s)'%regex)

    else:
        #search = TorrentSearch()
        finder = Torrent.objects.all()

    t_t = [ {
        't': f,
        'leech': f.clients.exclude(left = 0).count(),
        'seed' : f.clients.filter( left = 0 ).count(),
        } for f in finder]
    print t_t

    return render_to_response('tracker/torrent_search.html', {'torrents': t_t, 'query': query})

def torrent_list( request, category=None , page=1):
    list_category = Category.objects.all()
    step = 10
    page = int(page)
    prev_page = (page-1)*step
    next_page = page*step
    if category:
        temp = Torrent.objects.filter( category__name = category ).order_by('-creation_date')[prev_page:next_page]
    else:
        temp = Torrent.objects.all().order_by('-creation_date')[prev_page:next_page]


    t_t = [ {
        't': t,
        'leech': t.clients.exclude(left = 0).count(),
        'seed' : t.clients.filter( left = 0 ).count(),
        } for t in temp]
    stat ={
            's':Stat.objects.get(id=1),
            'leechs': Client.objects.exclude(left=0).count(),
            'seeds' : Client.objects.filter(left=0).count(),
            }
    return render_to_response('tracker/torrent_list.html',
            {
                'torrents': t_t,
                'stat': stat,
                'category': category,
                'page': page,
                'step': step,
                'num_page': { 'page':page, 'step':step, 'count': temp.count(), 'category': category, },
            })

def torrent_info( request, _id ):
    _i = Torrent.objects.filter(id=_id)
    if _i:
        _i = _i[0]
        if _i.announce_list:
            announce_list = _i.announce_list.split('|')
        else:
            announce_list = None
        if _i.file_list:
            from json import loads
            file_list = loads(_i.file_list)
        else:
            file_list = None
        info = { 't': _i,
                'leech': _i.clients.exclude(left = 0).count(),
                'seed' : _i.clients.filter( left = '0' ).count(),
                }
        #print announce_list
        return render_to_response('tracker/torrent_info.html', {'i': info, 'announce_list': announce_list, 'file_list': file_list })
    else:
        return HttpResponseNotFound('<h1>Page not found</h1>')


def torrent_add( request ):
    nocaptcha = 0
    error = None
    if request.method == 'POST':
        if not nocaptcha:
            check_captcha = captcha.submit(   request.POST['recaptcha_challenge_field'],
                    request.POST['recaptcha_response_field'],
                    settings.RECAPTCHA_PRIVATE_KEY, request.META['REMOTE_ADDR'])
            #print check_captcha.is_valid
            if not check_captcha.is_valid:
                pass
                return HttpResponseNotFound('<h1>You bot?</h1>')
        else: check_captcha = None

        form = TorrentAddForm( request.POST, request.FILES)
        if form.is_valid():

            anon = User.objects.get(id=1)
            instance = form.save( commit=False)
            instance.author = anon
            dublicate_id = instance.save()
            _id=instance.id
            if _id:
                return HttpResponseRedirect('/info/%i'%_id)
            else:
                error = "This torrent file is already in the database"
    else:
        form = TorrentAddForm()

    html_captcha = captcha.displayhtml(settings.RECAPTCHA_PUB_KEY)
    return render_to_response('tracker/torrent_add.html', {'form': form, 'recaptcha': html_captcha, 'error': error})















#-------------------------------------------------------------
'''
from django import forms

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file  = forms.FileField()



from django.shortcuts import render_to_response

def upload_torrent( request ):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        #form = TorrentForm(request.POST)#UploadTorrentForm( request.POST )
        print request.FILES.keys()
        #_add_torrent(request.FILES['file'])
        if form.is_multipart():
            pass
            #return HttpResponseRedirect('/success/url/')
    else:
        form = UploadFileForm()

#        form = TorrentForm()
    return render_to_response('add_torrent.html', {'form': form})

def _add_torrent(file):
    save = open('media/torrent/%s'%f.name, 'w')
    torrent = f.read()
    info_hash = _get_info_torrent(torrent)
    print info_hash
    try:
        t = Torrent.objects.get( info_hash = info_hash )
    except ObjectDoesNotExist:
        pass
#        t = Torrent.objects.create()


def _get_info_torrent(torrent):
    from hashlib import sha1
    torrent = hunnyb.decode(torrent)
    _hash = sha1(hunnyb.encode(torrent['info']))
    hash_base64 = base64.b64encode(_hash.digest())
    return hash_base64

'''
