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

    last_update = models.DateTimeField( auto_now=True, auto_now_add=True )
    def __unicode__(self):
        return  u'%s %s'%(self.user, self.ip)

class Category(models.Model):
    name = models.CharField(max_length=50)
    img_url = models.URLField( blank= True)
    img = models.ImageField( upload_to='image/category', blank=True)
    def __unicode__(self):
        return  u'%s'%self.name

class Torrent(models.Model):
    name = models.CharField(max_length=255, unique=True, db_index=True, blank=True)
    author = models.ForeignKey(User)
    file_path = models.FileField("File location", upload_to='torrents')
    clients = models.ManyToManyField(Client, blank=True)

    category = models.ForeignKey(Category)
    description = models.TextField( max_length=2048, blank= True)
    creation_date = models.DateTimeField(auto_now_add=True)
    completed = models.IntegerField( max_length = 6, default = 0)


    info_hash = models.CharField("Torrent info hash (base64)", max_length=40,blank=True)
    size = models.IntegerField("Size torrent", max_length=1024, blank=True)
    b_transfer = models.IntegerField("Bytes Transferred", max_length=1024,default=0, blank=True)

    #inactive_since = models.DateField(null=True, blank=True, editable=False)
    #f_active = models.BooleanField("Torrent enabled", default=True)
    #counts_seed = models.IntegerField("Counts seed", max_length=10,default=0, blank=True)
    #counts_leech = models.IntegerField("counts leech", max_length=10,default=0, blank=True)
    #counts_complete = models.IntegerField("counts leech", max_length=10,default=0, blank=True)
    #slug = models.SlugField( blank=True)#prepopulate_from=("pre_name", "name"))
    def __unicode__(self):
        return  u'%s'%self.name
    def save(self):
        #print "save torrent"
        #print self, dir(self)
        torrent = self.file_path
        torrent_path = torrent._get_path()
        if not torrent_path.endswith('.torrent'):
            print "this file not torrent"
        else:
            self.name, self.info_hash, self.size , torrent_file = _get_info_torrent( self.file_path._get_file().read() )
            f = open( torrent_path, 'w')
            f.write( torrent_file )
            f.close()
            stat= Stat.objects.get(id=1)
            stat.all_size += self.size
            print "test"
            super( Torrent, self).save()
            stat.save()
    def delete(self):
        stat = Stat.objects.get(id=1)
        stat.all_size -= self.size
        #print dir(self)
        super(Torrent, self).delete()
        #self.file_path.delete()
        stat.save()

class Stat(models.Model):
    all_size = models.IntegerField( max_length = 1024 ,default=0)
    seeds = models.IntegerField( max_length = 1024 ,default=0)
    leechs = models.IntegerField( max_length = 1024 ,default=0)
    completeds = models.IntegerField( max_length = 1024 ,default=0)
    b_transfers = models.IntegerField( max_length = 1024 ,default=0)
    speed = models.IntegerField( max_length = 1024 ,default=0)
    def save(self):
        self.seeds = Client.objects.filter(left=0).count()
        self.leechs = Client.objects.exclude(left=0).count()
        super( Stat, self).save()



def _get_info_torrent(torrent):
    from django.contrib.sites.admin import Site
    from hashlib import sha1
    import base64
    from simplebtt.tracker.benc import bencode, bdecode

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
