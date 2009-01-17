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
    def get_filenames_and_size(self, json=True):
        files = self.meta_info.get('files')
        if files:
            file_and_size = [ {
                'file':'/'.join(f.get('path.utf-8') or f.get('path')),
                'size': f['length']} for f in files ]
        else:
            file_and_size = [{
                'file': self.meta_info.get('name.utf-8') or self.meta_info.get('name') ,
                'size':self.meta_info['length']
                }]
        if json:
            from json import dumps
            return dumps( file_and_size )

        pass
    def get_all_announce_str(self, delimiter='|'):
        anon = [self.meta['announce']]
        anon_list = self.meta.get('announce-list')
        if anon_list:
            anon.extend( [ m[0] for m in anon_list])
        return delimiter.join(list(set(anon)))
    def add_in_announce_list(self, url, end=False):
        if self.meta.get('announce-list'):
            if end:
                self.meta['announce-list'].append([url])
            else:
                self.meta['announce-list'].insert(0,[url])
        else:
            self.meta['announce-list'] = [[url], [self.meta['announce']]]



if __name__ == '__main__':
    f = open('/home/apkawa/Code/test/download.torrent', 'r')
    tp = TorrentParser()
    tp.parse_file(f.read())
    f.close()
    print dir(tp)
    #print tp.meta
    #print tp.meta_info
    print tp.get_name()
    print tp.get_info_hash()
    print tp.get_info_hash_base64()
    print tp.get_size()
    print tp.meta['announce']
    #print tp.meta['announce-list']
    print tp.get_all_announce_str()
    tp.add_in_announce_list('http://nya.org.ru/lalalal')
    #print tp.meta['announce-list']
    print tp.get_filenames_and_size()
    print len(tp.get_filenames_and_size())
    #e = open('/home/apkawa/Code/test/test-nya.torrent', 'w')
    #e.write(tp.get_file())
    #e.close()


