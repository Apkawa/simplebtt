from simplebtt.tracker.models import Torrent, User, Client, Category
from django.contrib import admin
from simplebtt import settings
import hunnyb
from simplebtt.tracker.benc import bencode, bdecode

class UserAdmin(admin.ModelAdmin):
    list_display = ['aunt', 'passkey']

admin.site.register( User, UserAdmin)

class ClientAdmin(admin.ModelAdmin):
    #search_fields = ['foreignkey__related_user']
    list_display = ['ip','user']

admin.site.register( Client, ClientAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

admin.site.register( Category, CategoryAdmin)

class TorrentAdmin(admin.ModelAdmin):
    list_display = ['name']
    def save_model(self, request, obj, form, change):
        if request.FILES.keys():
            obj.name, obj.info_hash, obj.size , torrent_file = self._get_info_torrent( request.FILES['file_path'] )
            path = settings.MEDIA_ROOT+'/'+str(obj.file_path)
            f = open(path, 'w')
            f.write( torrent_file )
            f.close()
            obj.save()
        else:
            pass
            obj.save()
    def _get_info_torrent(self, torrent):
        from django.contrib.sites.admin import Site
        from hashlib import sha1
        import base64

        a = ''
        for chunk in torrent.chunks(): a = a+chunk

        torrent = bdecode(a)
        torrent['announce'] = 'http://%s/announce' %Site.objects.all()[0].domain
        torrent_file = bencode(torrent)
        _hash = sha1( bencode(torrent['info']))
        hash_base64 = base64.b64encode(_hash.digest())
        name = torrent['info']['name']
        size = torrent['info']['length']
        return name, hash_base64, size, torrent_file
#    prepopulated_fields = {'slug': ('name',) }

admin.site.register( Torrent, TorrentAdmin)
