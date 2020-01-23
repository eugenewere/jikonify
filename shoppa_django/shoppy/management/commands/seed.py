from django.core.management import BaseCommand

from shoppy.models import Category


class Command(BaseCommand):
    help = "seed database for testing and development."

    def add_arguments(self, parser):
        parser.add_argument('--mode', type=str, help="Mode")

    def handle(self, *args, **options):
        self.stdout.write('seeding data...')
        run_seed(self, options['mode'])
        self.stdout.write('done.')


def clear_data():
    """Deletes all the table data"""
    print("Delete all data instances")

    # model object to be deleted
    q_models = [
        # Category,
    ]

    for model in q_models:
        print("Deleted all {}".format(model))
        model.objects.all().delete()


def create_categories():
    """ Creates the root categories"""
    print("Creating Root Categories")
    return "Done"


def run_seed(self, mode):
    """ Seed database based on mode

    :param mode: refresh / clear
    :return:
    """
    mode_clear = "fresh"
    # Clear data from tables
    if mode == mode_clear:
        clear_data()

    create_categories()
    pass

