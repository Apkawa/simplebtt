from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from simplebtt.tracker.models import Torrent, User, Client, Stat

from urllib import unquote
from re import findall
import base64
from simplebtt.tracker.benc import bencode
import datetime

def _stat( t, c, client):
    stat = Stat.objects.get(id=1)
    transfer = (client['downloaded']-c.dl)+(client['uploaded']-c.ul)
    if t.b_transfer:
        if t.b_transfer != transfer:
            t.b_transfer += transfer
            stat.b_transfers += transfer
    else:
        t.b_transfer = transfer
    if client['event'] == 'stopped':
        c.delete()

    elif c.left != client['left']:
        c.dl, c.ul, k.left = client['downloaded'], client['uploaded'], client['left']
        if c.left != client['left'] and c.left == '0':
            t.completed += 1
            stat.completeds += 1

    elif c.ip != client['ip']:
        c.ip = client['ip']


def main( request):
    def _fail(fail):
        return HttpResponse( bencode({'failure reason': fail}))

    client = {}
    if not request.GET.items() or not request.GET.get('info_hash'):
        return HttpResponse("This file is for BitTorrent clients.")

    get_str = request.META['QUERY_STRING']

    client['ip']=request.GET.get('ip',None) or request.META['REMOTE_ADDR'] #
    client['port'] = int(request.GET.get('port'))

    client['info_hash'] = findall('info_hash=(.*?)&', get_str)
    client['peer_id'] = findall('peer_id=(.*?)&',get_str)[0]

    client['event'] = request.GET.get('event')
    client['uploaded'] = int(request.GET.get('uploaded'))
    client['downloaded'] = int(request.GET.get('downloaded'))
    client['left'] = int(request.GET.get('left'))

    client['passkey'] = 'none'
    #now = datetime.datetime.now


    banned_client = ('OP','FUTB','exbc','-TS','Mbrst','-BB','-SZ','turbo','T03A','T03B','FRS','eX','-TR0005-','-TR0006-','-XX0025-','-AG','R34',)
    for ban in banned_client:
        if client['peer_id'].startswith(ban):
            return _fail('This is a banned client.')
    try:
        u = User.objects.get(passkey=client['passkey'])
    except ObjectDoesNotExist:
        return _fail('Invalid passkey, please redownload torrent')

    _hash = base64.b64encode(str( unquote( client['info_hash'][0] )))
    try:
        t = Torrent.objects.get(info_hash=_hash)
    except ObjectDoesNotExist:
        return _fail('Torrent does not exist')

    _client ={ 'user' : u,
                    'ip' : client['ip'],
                    'port' : client['port'],
                    'dl':client['downloaded'],
                    'ul':client['uploaded'],
                    'left' : client['left'],
                    }
    c = t.clients.get_or_create(peer_id=client['peer_id'], defaults=_client)[0]

    _stat(t, c, client)

    t.save()

    clients = [{'ip': i.ip, 'peer id': unquote( i.peer_id ), 'port': i.port} for i in t.clients.all()]
    r = {'peers': clients, 'interval': 1800}

    return HttpResponse( bencode(r))
'''
    try:
        #if a user already eists, we're good.
        _client ={ 'user' : u,
                    'ip' : client['ip'],
                    'port' : client['port'],
                    'dl':client['downloaded'],
                    'ul':client['uploaded'],
                    'left' : client['left'],
                    }
        #k = t.objects.get_or_create(peer_id=client['peer_id'])
        transfer = (client['downloaded']-k.dl)+(client['uploaded']-k.ul)
        if t.b_transfer:
            if t.b_transfer != transfer:
                t.b_transfer += transfer
                stat.b_transfers += transfer
        else:
            t.b_transfer = transfer
        if client['event'] == 'stopped':
            k.delete()

        elif k.left != client['left']:
            k.dl, k.ul, k.left = client['downloaded'], client['uploaded'], client['left']
            if k.left != client['left'] and k.left == '0':
                t.completed += 1
                stat.completeds += 1

        elif k.ip != client['ip']:
            k.ip = client['ip']

    except ObjectDoesNotExist:
        #if the user doesn't exist, create one
        if client['event'] == 'stopped':
            pass
        else:
            t.clients.create(user=u, ip=client['ip'], port=client['port'],
                    peer_id=client['peer_id'], dl=client['downloaded'], ul=client['uploaded'], left = client['left'])# , last_update = now().time())

'''


