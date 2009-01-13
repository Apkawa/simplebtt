#from django.contrib.sites.admin import Site
from hashlib import sha1
import base64
from benc import bencode, bdecode

class TorrentParser:
    meta = {}
    meta_info = {}
    def __init__(self):
        pass
    def parse_file(self, _file ):
        self.meta = bdecode(_file)
        self.meta_info = self.meta['info']
    def get_name(self):
        return self.meta_info['name']
    def get_info_hash(self):
        return sha1( bencode(self.meta_info)).digest()
    def get_info_hash_base64(self):
        return base64.b64encode(self.get_info_hash())
    def get_size(self):
        files = self.meta_info.get('files')
        if files:
            return sum([f['length'] for f in files])
        else:
            return self.meta_info['length']
    def get_file(self):
        return bencode(self.meta)
    def add_in_announce_list(self, url, end=False):
        if self.meta.get('announce-list'):
            if end:
                self.meta['announce-list'].append([url])
            else:
                self.meta['announce-list'].insert(0,[url])
        else:
            self.meta['announce-list'] = [[url],]

        pass



def _get_info_torrent(torrent):

    a = torrent
    torrent = bdecode(a)
    torrent['announce'] = 'http://%s/announce' %Site.objects.all()[0].domain
    torrent_file = bencode(torrent)
    _hash = sha1( bencode(torrent['info']))
    hash_base64 = base64.b64encode(_hash.digest())
    name = torrent['info']['name']
    files = torrent['info'].get('files')
    size = 0
    if files:
        for f in files:
            size += f['length']
    else:
        size = torrent['info']['length']
    return name, hash_base64, size, torrent_file

if __name__ == '__main__':
    f = open('/home/apkawa/Code/test/download.torrent', 'r')
    tp = TorrentParser()
    tp.parse_file(f.read())
    f.close()
    print dir(tp)
    print tp.get_name()
    print tp.get_info_hash()
    print tp.get_info_hash_base64()
    print tp.get_size()
    print tp.meta['announce']
    print tp.meta['announce-list']
    tp.add_in_announce_list('http://nya.org.ru/lalalal')
    print tp.meta['announce-list']
    e = open('/home/apkawa/Code/test/test-nya.torrent', 'w')
    e.write(tp.get_file())
    e.close()


