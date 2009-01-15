from simplebtt.tracker.models import Torrent, User, Client, Category, Stat
from django.contrib import admin

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
    list_display = ['name','t_remove']

admin.site.register( Torrent, TorrentAdmin)

class StatAdmin( admin.ModelAdmin):
    list_display = ['id','all_size','all_torrents']
admin.site.register( Stat, StatAdmin)

