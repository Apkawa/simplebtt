from django.http import HttpResponse, HttpResponseNotFound
from django.core.exceptions import ObjectDoesNotExist
from django.utils.encoding import DjangoUnicodeDecodeError
from simplebtt.tracker.models import Torrent, User, Client, TorrentForm

from urllib import unquote
from re import findall
import base64
#import hunnyb
from benc import bencode


def torrent_list( request ):
    temp = Torrent.objects.all()
    t_t = [ {
        'id' : t.id,
        'category' : t.category.name,
        'name':t.name,
        'file_path' : t.file_path,
        'size' : t.size,
        'date' : t.creation_date,
        'desc' : t.description,
        'leech': t.clients.exclude(left = 0).count(),
        'seed' : t.clients.filter( left = '0' ).count(),
        'complete' : t.completed,
        'b_transfer' : t.b_transfer,
        } for t in temp]
    return render_to_response('torrent_list.html', {'torrents': t_t})

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














#-------------------------------------------------------------

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


