from django.core.management.base import BaseCommand, CommandError
from stock.models import StockManager


class Command(BaseCommand):
    help = 'Updates database (use when stocks have been bought or sold)'

    # def add_arguments(self, parser):
    #    parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        return StockManager.update(self)
