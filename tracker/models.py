from django.db import models

# Create your models here.
class User(models.Model):
    #auth = models.OneToOneField(auth_models.User, verbose_name="Django auth user")
    aunt = models.CharField("User_name", max_length=40)
    passkey = models.CharField("Torrent passkey", max_length=40)
    #immune = models.BooleanField("Immune from auto-pruning", default=False)
    def __unicode__(self):
        return u'%s'%self.aunt

class Client(models.Model):
    ip = models.IPAddressField()
    port = models.IntegerField( max_length=7)
    user = models.ForeignKey(User)
    peer_id = models.CharField(max_length=50)
    dl = models.IntegerField( max_length=1024 )
    ul = models.IntegerField( max_length=1024 )
    left = models.IntegerField( max_length=1024 ) #left = 0  - seeder else leacher
    def __unicode__(self):
        return  u'%s %s'%(self.user, self.ip)

class Category(models.Model):
    name = models.CharField(max_length=255)
    def __unicode__(self):
        return  u'%s'%self.name

class Torrent(models.Model):
    name = models.CharField(max_length=255, unique=True, db_index=True, blank=True)
    author = models.ForeignKey(User)
    file_path = models.FileField("File location", upload_to='media/torrents')
    inactive_since = models.DateField(null=True, blank=True, editable=False)
    clients = models.ManyToManyField(Client, blank=True)
    category = models.ForeignKey(Category)
    #f_active = models.BooleanField("Torrent enabled", default=True)

    info_hash = models.CharField("Torrent info hash (base64)", max_length=40,blank=True)
    size = models.IntegerField("Size torrent", max_length=1024, blank=True)
    b_transfer = models.IntegerField("Bytes Transferred", max_length=1024,default=0, blank=True)

    counts_seed = models.IntegerField("Counts seed", max_length=10,default=0, blank=True)
    counts_leech = models.IntegerField("counts leech", max_length=10,default=0, blank=True)
    counts_complete = models.IntegerField("counts leech", max_length=10,default=0, blank=True)
    #slug = models.SlugField( blank=True)#prepopulate_from=("pre_name", "name"))
    def __unicode__(self):
        return  u'%s'%self.name

from django.forms import ModelForm
class TorrentForm(ModelForm):
    class Meta:
        model = Torrent
        exclude = ('clients','info_hash','slug','inactive_since','author','f_active')


