import logging

from celery import task

from directory.itunes_adapter import update_podcast_by_id

logger = logging.getLogger(__name__)

@task(name="update_itunes_podcast")
def update_itunes_podcast(itunes_id):
    return update_podcast_by_id(itunes_id)
