import json
import logging
import urllib

from pprint import pprint
from directory.models import *

# logger = logging.getLogger(__name__)


def import_ids(json_file):
    with open('/home/tbartel/Projects/podback/result.json') as data_file:
        count = 0
        data = json.load(data_file)
        for podcast in data:
            count += 1
            itunes_podcast, created = Itunes.objects.get_or_create(collection_id=podcast['itunesId'])
            if created:
                itunes_podcast.collection_name = podcast['name'].encode("UTF-8")
                itunes_podcast.collection_view_url = podcast['url']
                itunes_podcast.save()
                pprint(u'%s : Imported "%s" successfully' % (count, podcast['name'].encode("UTF-8")) )
            else:
                pprint('%s : Skipped "%s - %s"' % (count, podcast['itunesId'], podcast['name']) )


def update_podcast_by_id(itunes_ids):
    try:
        response = urllib.urlopen("https://itunes.apple.com/lookup?id=%s" % itunes_ids)
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
            pprint("Podcast \'%s - %s\' updated from the iTunes directory." % (one_podcast.collection_id, one_podcast.collection_name))
            #logger.info("Podcast \'%s - %s\' updated from the iTunes directory." % (one_podcast.collection_id, one_podcast.collection_name))
        return True
    except Exception as inst:
        #logger.error("Could not update iTunes IDs: %s (%s - %s)" % (itunes_ids, type(inst), inst.args))
        pprint("Could not update iTunes IDs: %s (%s - %s)" % (itunes_ids, type(inst), inst.args))
        return False


def handle_country(country_name):
    itunes_country, created = ItunesCountry.objects.get_or_create(name=country_name)
    return itunes_country


def handle_genre(genre_ids, genre_names):
    my_genres = []
    for key, number in enumerate(genre_ids):
        itunes_genre, created = ItunesGenre.objects.get_or_create(number=number, name=genre_names[key])
        my_genres.append(itunes_genre)
    return my_genres


def handle_primary_genre(name):
    try:
        itunes_genre = ItunesGenre.objects.get(name=name)
        return itunes_genre
    except:
        logger.exception("Primary genre was \'%s\' not found in the database." % name)
        return None
