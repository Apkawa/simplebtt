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
    dl = models.IntegerField( max_length=1024, default=0)
    ul = models.IntegerField( max_length=1024, default=0)
    left = models.IntegerField( max_length=1024, default=0) #left = 0  - seeder else leacher

    speed = models.IntegerField( max_length=1024, default=0 )

    last_update = models.DateTimeField( auto_now=True, auto_now_add=True )
    def __unicode__(self):
        return  u'%s %s'%(self.user, self.ip)

    #def save(self):
    #    cit = self.torrent_set.all()[0].clients
    #    self.seeds = cit.filter(left=0).count()
    #    self.leechs = cit.exclude(left=0).count()
    #    super( Stat, self).save()

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
    speed = models.IntegerField(max_length=1024,default=0, blank=True)
    announce_list = models.CharField(max_length=1024,blank=True)
    file_list = models.CharField(max_length=1048576, blank=True)

    def __unicode__(self):
        return  u'%s'%self.name

    def t_remove(self):
        return '<a href="%s/delete/" class="deletelink">Delete</a>' % self.id
    t_remove.allow_tags = True


    def save(self):
        #print self, dir(self)
        torrent = self.file_path
        torrent_path = torrent._get_path()
        if not torrent_path.endswith('.torrent'):
            print "this file not torrent"
            return False
        elif not self.id:
            from torrent_parser import TorrentParser
            from django.contrib.sites.admin import Site
            announce_url = 'http://%s/announce' %Site.objects.all()[0].domain
            tp = TorrentParser()
            tp.parse_file( self.file_path._get_file().read())
            self.info_hash = tp.get_info_hash_base64()
            if Torrent.objects.filter(info_hash = self.info_hash ):
                return False
            self.name = unicode(tp.get_name(), 'utf-8')
            self.size = tp.get_size()
            self.file_list = tp.get_filenames_and_size()
            tp.add_in_announce_list( announce_url  )
            tp.meta['announce'] = announce_url
            self.announce_list = tp.get_all_announce_str()
            f = open( torrent_path, 'w')
            f.write( tp.get_file() )
            f.close()
            stat = Stat.objects.get(id = 1)
            stat.all_size += self.size
            super( Torrent, self).save()
            stat.all_torrents = Torrent.objects.all().count()
            stat.save()
        else:
            super( Torrent, self).save()

    def delete(self):
        stat = Stat.objects.get(id=1)
        stat.all_size -= self.size
        super(Torrent, self).delete()
        stat.save()


class Stat(models.Model):
    all_size = models.IntegerField( max_length = 1024 ,default=0)
    all_torrents  = models.IntegerField( max_length = 1024 ,default=0)
    seeds = models.IntegerField( max_length = 1024 ,default=0)
    leechs = models.IntegerField( max_length = 1024 ,default=0)
    completeds = models.IntegerField( max_length = 1024 ,default=0)
    b_transfers = models.IntegerField( max_length = 1024 ,default=0)
    speeds = models.IntegerField( max_length = 1024 ,default=0)



