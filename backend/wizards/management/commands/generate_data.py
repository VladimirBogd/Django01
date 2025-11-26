from django.core.management.base import BaseCommand
import random
from faker import Faker

from django.contrib.auth.models import User
from wizards.models import Wizard, Guild, Order, Customer, Team

class Command(BaseCommand):
    def handle(self, *args, **options):
        fake = Faker(['ru_RU'])
        
        # Генерация гильдий
        for _ in range(5):  # Создаем 5 гильдий
            Guild.objects.create(
                name=fake.company()
            )

        guilds = Guild.objects.all()
        
        # Генерация команд
        for _ in range(10):  # Создаем 10 команд
            random_guild = random.choice(guilds) if guilds else None
            Team.objects.create(
                name=fake.word(),
                guild=random_guild
            )
        
        teams = Team.objects.all()
        
        # Генерация пользователей
        for _ in range(5):  # Создаем 5 пользователей
            user = User.objects.create_user(
                username=fake.user_name(),
                email=fake.email(),
                password='password123'
            )
            Customer.objects.create(
                user=user,
                username=user.username,
                email=user.email,
                first_name=fake.first_name(),
                last_name=fake.last_name()
            )

        customers = Customer.objects.all()
        users = User.objects.all()

        # Генерация волшебников
        for _ in range(10):  # Создаем 10 волшебников
            random_guild = random.choice(guilds) if guilds else None
            random_team = random.choice(teams) if teams else None
            
            Wizard.objects.create(
                name=fake.name(),
                guild=random_guild,
                team=random_team
            )

        # Генерация заказов
        for _ in range(15):  # Создаем 15 заказов
            random_customer = random.choice(customers) if customers else None
            random_guild = random.choice(guilds) if guilds else None
            random_team = random.choice(teams) if teams else None
            random_user = random.choice(users) if users else None
            
            Order.objects.create(
                name=fake.catch_phrase(),
                cost=fake.random_number(digits=4),
                customer=random_customer,
                guild=random_guild,
                team=random_team,
                user=random_user
            )
