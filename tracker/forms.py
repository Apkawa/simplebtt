from django import forms
from simplebtt.tracker.models import Torrent#, User, Client, Stat, Category# TorrentForm

class TorrentAddForm( forms.ModelForm):
    class Meta:
        model = Torrent
        fields = ['file_path','category', 'description']

class TorrentSearch( forms.Form ):
    search = forms.CharField(max_length=50)
