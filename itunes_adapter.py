from main.settings import DEBUG
from directory.models import Itunes, ItunesGenre, ItunesCountry
from pprint import pprint
import json, urllib
from time import sleep
import logging

logger = logging.getLogger(__name__)

def import_ids(json_file):
    with open('/home/tbartel/Projects/podback/result.json') as data_file:
      data = json.load(data_file)
      for podcast in data:
        try:
          itunes_podcast = Itunes.objects.get(collection_id=podcast['itunesId'])
        except Itunes.DoesNotExist:
          itunes_podcast = Itunes(collection_id=podcast['itunesId'])

        itunes_podcast.collection_name=podcast['name']
        itunes_podcast.collection_view_url=podcast['url']
        itunes_podcast.save()
        logger.info('Processed "%s" successfully' % json_file)

def update_all_podcasts():
  for one_podcast in Itunes.objects.all().order_by('-modified'):
      logger.info('Updating \'%s\'' % one_podcast)
      itunes_id = one_podcast.collection_id
      if DEBUG:
        pprint(update_podcast_by_id(itunes_id))
      else:
        update_itunes_podcast.delay(itunes_id)

def update_podcast_by_id(itunes_id):
    try:
        response = urllib.urlopen("https://itunes.apple.com/lookup?id=%s" % itunes_id)
        json_data = json.loads(response.read())
        for podcast_data in json_data['results']:
            one_podcast = Itunes.objects.get(collection_id=podcast_data['collectionId'])
            one_podcast.collection_name = podcast_data['collectionName']
            one_podcast.collection_ensored_name = podcast_data['collectionCensoredName']
            one_podcast.collection_explicitness = podcast_data['trackExplicitness']
            if 'contentAdvisoryRating' in podcast_data:
               one_podcast.content_advisory_rating = podcast_data['contentAdvisoryRating']
            one_podcast.country = handle_country(podcast_data['country'])
            one_podcast.genre = handle_genre(podcast_data['genreIds'], podcast_data['genres'])
            one_podcast.primary_genre = handle_primary_genre(podcast_data['primaryGenreName'])
            one_podcast.feed_url = podcast_data['feedUrl']
            if 'releaseDate' in podcast_data:
               one_podcast.release_date = podcast_data['releaseDate']
            one_podcast.collection_view_url = podcast_data['collectionViewUrl']
            one_podcast.artist_name = podcast_data['artistName']
            one_podcast.artwork_30 = podcast_data['artworkUrl30']
            one_podcast.artwork_60 = podcast_data['artworkUrl60']
            one_podcast.artwork_100 = podcast_data['artworkUrl100']
            one_podcast.artwork_600 = podcast_data['artworkUrl600']
            one_podcast.save()
            logger.info("Podcast \'%s - %s\' updated from the iTunes directory." % (one_podcast.collection_id, one_podcast.collection_name))
        return True
    except:
        logger.error("Could not update \'%s\'" % itunes_id)
        return False

def handle_country(country_name):
  try:
    itunes_country = ItunesCountry.objects.get(name=country_name)
  except ItunesCountry.DoesNotExist:
    itunes_country = ItunesCountry(name=country_name)
  itunes_country.save()
  return itunes_country

def handle_genre(genre_ids, genre_names):
  my_genres = []
  for key, number in enumerate(genre_ids):
    try:
      itunes_genre = ItunesGenre.objects.get(number=number)
    except:
      itunes_genre = ItunesGenre(number=number, name=genre_names[key])
      itunes_genre.save()
    my_genres.append(itunes_genre)
    return my_genres

def handle_primary_genre(name):
  try:
      itunes_genre = ItunesGenre.objects.get(name=name)
      return itunes_genre
  except:
      logger.exception("Primary genre was \'%s\' not found in the database." % name)
      return null
