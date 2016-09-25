from __future__ import unicode_literals
from django.utils import timezone
from django.db import models

class Itunes(models.Model):
    collection_id = models.BigIntegerField(db_index=True)
    collection_name = models.CharField(max_length=1000, null=True, blank=True)
    collection_ensored_name = models.CharField(max_length=1000, null=True, blank=True)
    collection_explicitness = models.CharField(max_length=20, null=True, blank=True)
    content_advisory_rating = models.CharField(max_length=20, null=True, blank=True)
    country = models.ForeignKey('ItunesCountry', null=True, blank=True)
    genre = models.ManyToManyField('ItunesGenre', blank=True)
    primary_genre = models.ForeignKey('ItunesGenre', related_name='primary_genre', null=True, blank=True)
    feed_url = models.URLField(null = True, blank=True)
    release_date = models.DateTimeField(null=True, blank=True)
    collection_view_url = models.URLField(null = True, blank=True)
    artist_name = models.CharField(max_length=1000, null=True, blank=True)
    artwork_30 = models.URLField(null = True, blank=True)
    artwork_60 = models.URLField(null = True, blank=True)
    artwork_100 = models.URLField(null = True, blank=True)
    artwork_600 = models.URLField(null = True, blank=True)
    created     = models.DateTimeField(editable=False, auto_now_add=True, db_index=True)
    modified    = models.DateTimeField(auto_now=True, db_index=True)

    def __unicode__(self):
        return unicode(self.collection_name)

class ItunesGenre(models.Model):
  number = models.PositiveIntegerField(db_index=True)
  name = models.CharField(max_length=200, db_index=True)

  def __unicode__(self):
    return unicode(self.name)

class ItunesCountry(models.Model):
  name = models.CharField(max_length=20, db_index=True)

  def __unicode__(self):
      return unicode(self.name)
