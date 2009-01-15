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

    elif request.method == 'POST':
        search = TorrentSearch( request.POST )
        if search.is_valid():
            #print dir(search)
            import re
            query = search.cleaned_data['search']
            regex = '!|'.join(re.sub('([\s]+|\n+)',' ', query).split(' '))
            finder = Torrent.objects.filter( name__iregex = r'(%s)'%regex)

    else:
        search = TorrentSearch()
        finder = Torrent.objects.all()

    t_t = [ {
        't': f,
        'leech': f.clients.exclude(left = 0).count(),
        'seed' : f.clients.filter( left = 0 ).count(),
        } for f in finder]
    print t_t

    return render_to_response('tracker/torrent_list.html', {'torrents': t_t,})

def torrent_list( request, category=None ):
    list_category = Category.objects.all()
    temp = Torrent.objects.all()
    #search = TorrentSearch()

    if category:
        temp = temp.filter( category__name = category )
        #search = TorrentSearch()

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
    return render_to_response('tracker/torrent_list.html', {'torrents': t_t, 'stat': stat, 'category': list_category,})

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
    #from random import _urandom
    #from hashlib import sha1
    #_prefix = sha1(_urandom(20)).hexdigest()
    print request.POST
    print "nya!!!"
    if request.method == 'POST':
        check_captcha = captcha.submit(
                request.POST['recaptcha_challenge_field'],
                request.POST['recaptcha_response_field'],
                settings.RECAPTCHA_PRIVATE_KEY, request.META['REMOTE_ADDR'])
        print check_captcha.is_valid
        if not check_captcha.is_valid:
            return HttpResponseNotFound('<h1>You bot?</h1>')

        form = TorrentAddForm( request.POST, request.FILES)
        if form.is_valid:

            anon = User.objects.get(id=1)
            instance = form.save( commit=False)
            instance.author = anon
            instance.save()
            _id=instance.id
            print _id
            return HttpResponseRedirect('/info/%i'%_id)
        else:
            return HttpResponseNotFound('<h1>Form not valid</h1>')

    else:
        form = TorrentAddForm()
        html_captcha = captcha.displayhtml(settings.RECAPTCHA_PUB_KEY)
    return render_to_response('tracker/torrent_add.html', {'form': form, 'recaptcha': html_captcha})















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
