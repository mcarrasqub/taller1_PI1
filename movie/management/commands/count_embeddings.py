from django.core.management.base import BaseCommand
from movie.models import Movie

class Command(BaseCommand):
    help = 'Cuenta cuántas películas tienen embeddings guardados.'

    def handle(self, *args, **kwargs):
        total = Movie.objects.count()
        with_emb = Movie.objects.exclude(emb=None).count()
        self.stdout.write(self.style.SUCCESS(f"Películas con embedding: {with_emb} de {total}"))
