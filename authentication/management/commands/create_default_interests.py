from django.core.management.base import BaseCommand
from authentication.models import Interest

class Command(BaseCommand):
    help="Creates default interests"
    def handle(self,*args,**kwargs):
        interests=['Art','Business','Gamimg','Education','Entertainment','Food','Health','History','Reading','Men fashion','Women fashion','Politics','Science','Sports','Technology','Travel']
        for interest in interests:
            Interest.objects.create(name=interest)
        print("Default interests created")