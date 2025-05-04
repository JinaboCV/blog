from django.core.management.base import BaseCommand
from django_seed import Seed
from blogs.models import Category, Writer, Tag, Article
from django.contrib.auth.models import User
import random



class Command(BaseCommand):
    help = 'Seed the database with dummy data for Writers, Categories, Tags, and Articles.'

    def handle(self, *args, **kwargs):
        seeder = Seed.seeder()

        # Seed Writers - Create User for each Writer
        seeder.add_entity(Writer, 2, {
            'phone': lambda x: seeder.faker.phone_number(),
            'bio': lambda x: seeder.faker.text(),
            'user': lambda x: User.objects.create_user(
                username=seeder.faker.user_name(),
                email=seeder.faker.unique.email(),
                password='password123'  # Ensure users have passwords for auth
            )
        })

        # Seed Categories
        seeder.add_entity(Category, 3, {
            'title': lambda x: seeder.faker.unique.word(),
            'description': lambda x: seeder.faker.text(max_nb_chars=100),
        })

        # Seed Tags
        seeder.add_entity(Tag, 3, {
            'name': lambda x: seeder.faker.word(),
        })

        # Execute seeding and get inserted primary keys
        seeder.execute()

        # Fetch created objects
        writers = Writer.objects.all()
        categories = Category.objects.all()
        tags = list(Tag.objects.all())

        # Create Articles manually
        for _ in range(8):
            article = Article.objects.create(
                author=random.choice(writers),  # Use the User associated with Writer
                category=random.choice(categories),
                title=seeder.faker.sentence(nb_words=8),
                thumbnail='default.jpg',  # Adjust based on your media setup
                content=seeder.faker.paragraph(nb_sentences=500),
            )
            article.tags.set(random.sample(tags, random.randint(1, 3)))  # Assign tags randomly

        self.stdout.write(self.style.SUCCESS('✅ Seeded Writers, Categories, Tags, and Articles (slug handled automatically).'))
