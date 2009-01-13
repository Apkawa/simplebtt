from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.utils.encoding import DjangoUnicodeDecodeError
from simplebtt.tracker.models import Torrent, User, Client, Stat, Category# TorrentForm
from django.shortcuts import render_to_response

from urllib import unquote
from re import findall
import base64
#import hunnyb
from benc import bencode


def torrent_list( request, category=None ):

    list_category = Category.objects.all()
    temp = Torrent.objects.all()
    count_all_torrent = temp.count()
    if category:
        temp = temp.filter( category__name = category )

    t_t = [ {
        't': t,
        'leech': t.clients.exclude(left = 0).count(),
        'seed' : t.clients.filter( left = 0 ).count(),
        } for t in temp]
    stat ={
            #'s':Stat.objects.get(id=1),
            #'leechs': Client.objects.exclude(left=0).count(),
            #'seeds' : Client.objects.filter(left=0).count(),
            }
    return render_to_response('torrent_list.html', {'torrents': t_t, 'stat': stat, 'category': list_category, 'count_all_torrent': count_all_torrent,})

def torrent_info( request, _id ):
    _i = Torrent.objects.filter(id=_id)
    if _i:
        _i = _i[0]
        info = { 't': _i,
                'leech': _i.clients.exclude(left = 0).count(),
                'seed' : _i.clients.filter( left = '0' ).count(),
                }
        return render_to_response('torrent_info.html', {'i': info})
    else:
        return HttpResponseNotFound('<h1>Page not found</h1>')

from django.forms import ModelForm
class TorrentAddForm( ModelForm):
    class Meta:
        model = Torrent
        fields = ['file_path','category', 'description']#,'author']

def torrent_add( request ):
    #from random import _urandom
    #from hashlib import sha1
    #_prefix = sha1(_urandom(20)).hexdigest()
    if request.method == 'POST':
        print request.POST.keys()
        print dir(request.FILES)
        anon = User.objects.get(id=1)
        form = TorrentAddForm( request.POST, request.FILES)
        instance = form.save( commit=False)
        instance.author = anon
        instance.save()
        _id=instance.id
        return HttpResponseRedirect('/info/%i'%_id)

    else:
        form = TorrentAddForm()
    return render_to_response('add_torrent.html', {'form': form})















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
