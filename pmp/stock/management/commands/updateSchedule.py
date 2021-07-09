from django.core.management.base import BaseCommand, CommandError
from stock.models import StockManager
from stock.models import Stock

class Command(BaseCommand):
    help = 'Updates PMP Meeting Schedule'

    #def add_arguments(self, parser):
    #    parser.add_argument('poll_ids', nargs='+', type=int)
    
    def handle(self, *args, **options):
        return StockManager.updateSchedule(self)
