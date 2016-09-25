from directory.models import Itunes, ItunesGenre, ItunesCountry
from directory.itunes_adapter import update_podcast_by_id
from pprint import pprint
import json, urllib
from time import sleep
from celery import task
import logging

logger = logging.getLogger(__name__)

@task(name="update_itunes_podcast")
def update_itunes_podcast(itunes_id):
    return update_podcast_by_id(itunes_id)
