from django.core.management.base import BaseCommand, CommandError
from directory.models import Itunes, ItunesGenre, ItunesCountry
from directory.tasks import update_itunes_podcast
from directory.itunes_adapter import update_podcast_by_id
import json, urllib
from pprint import pprint
from time import sleep
import logging
from main.settings import DEBUG
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):
        for one_podcast in Itunes.objects.all().order_by('-modified'):
            logger.info('Updating \'%s\'' % one_podcast)
            itunes_id = one_podcast.collection_id
            if DEBUG:
                pprint(update_podcast_by_id(itunes_id))
            else:
                update_itunes_podcast.delay(itunes_id)