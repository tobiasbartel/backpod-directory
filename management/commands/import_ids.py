from django.core.management.base import BaseCommand, CommandError
from directory.models import Itunes
from directory.itunes_adapter import  import_ids
import json
from pprint import pprint

class Command(BaseCommand):
    help = ''

    def add_arguments(self, parser):
        parser.add_argument('file', nargs='+', type=str)

    def handle(self, *args, **options):
        import_ids(options['file'])
