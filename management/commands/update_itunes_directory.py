import logging

from django.core.management.base import BaseCommand
from django.core.paginator import Paginator

from directory.itunes_adapter import update_podcast_by_id
from directory.models import Itunes
from directory.tasks import update_itunes_podcast
from main.settings import DEBUG

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):
        all_podcasts = Itunes.objects.all().order_by('-modified')
        paginator = Paginator(all_podcasts, 200)
        for my_page in paginator.page_range:
            my_itunes_ids_list = []
            for one_object in paginator.page(my_page):
                my_itunes_ids_list.append(one_object.collection_id)
                my_itunes_ids_string = ','.join(map(str, my_itunes_ids_list))

            if DEBUG:
                update_podcast_by_id(my_itunes_ids_string)
            else:
                update_itunes_podcast.delay(my_itunes_ids_string)
