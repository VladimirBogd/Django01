from django.test import TestCase
from rest_framework.test import APIClient
from model_bakery import baker

from wizards.models import Wizard, Guild, Order, Customer, Team

class WizardsViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list(self):
        r = self.client.get('/api/wizards/')
        print(r)

    def test_get_wizard(self):
        gld = Guild.objects.create(
            name = "Blue Pegasus"
        )
        
        tm = Team.objects.create(
            name = "Team 1",
            guild = gld,
        )
        
        wizard = Wizard.objects.create(
            name="Hibiki Lates",
            team = tm,
            guild = gld,
        )

        r = self.client.get('/api/wizards/')
        data = r.json()
        print(data)

        assert wizard.name == data[0]['name']
        assert wizard.id == data[0]['id']
        assert wizard.team.id == data[0]['team']
        assert wizard.guild.id == data[0]['guild']
        assert len(data) == 1

    def test_create_wizard(self):
        gld = baker.make("wizards.Guild")
        tm = baker.make("wizards.Team")

        r = self.client.post("/api/wizards/", {
            "name": "Hibiki Lates",
            "team": tm.id,
            "guild": gld.id
        })

        new_wizard_id = r.json()['id']
        wizards = Wizard.objects.all()
        assert len(wizards) == 1

        new_wizard = Wizard.objects.filter(id=new_wizard_id).first()
        assert new_wizard.name == 'Hibiki Lates'
        assert new_wizard.team == tm
        assert new_wizard.guild == gld

    def test_delete_wizard(self):
        wizards = baker.make("Wizard", 10)
        r = self.client.get('/api/wizards/')
        data = r.json()
        assert len(data) == 10

        wizard_id_to_delete = wizards[3].id
        self.client.delete(f'/api/wizards/{wizard_id_to_delete}/')

        r = self.client.get('/api/wizards/')
        data = r.json()
        assert len(data) == 9

        assert wizard_id_to_delete not in [i['id'] for i in data]

    def test_update_wizard(self):
        guild = baker.make('Guild', name="Blue Pegasus")
        team = baker.make('Team', name="Team 1")
        wizard = baker.make('Wizard', name="Laxus Dreyar", guild=guild, team=team)

        r = self.client.get(f'/api/wizards/{wizard.id}/')
        data = r.json()
        assert data['name'] == wizard.name

        r = self.client.put(f'/api/wizards/{wizard.id}/', {
            "name": "Laxus Dreyar",
            "guild": wizard.guild.id,
            "team": wizard.team.id
        })
        assert r.status_code == 200

        r = self.client.get(f'/api/wizards/{wizard.id}/')
        data = r.json()
        assert data['name'] == 'Laxus Dreyar'

        wizard.refresh_from_db()
        assert data['name'] == wizard.name

class TeamsViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list(self):
        r = self.client.get('/api/teams/')
        print(r)

    def test_get_team(self):
        gld = Guild.objects.create(
            name = "Blue Pegasus"
        )
        
        team = Team.objects.create(
            name="Team 1",
            guild = gld,
        )

        r = self.client.get('/api/teams/')
        data = r.json()
        print(data)

        assert team.name == data[0]['name']
        assert team.id == data[0]['id']
        assert team.guild.id == data[0]['guild']
        assert len(data) == 1

    def test_create_team(self):
        gld = baker.make("Guild")
        
        r = self.client.post("/api/teams/", {
            "name": "Team 1",
            "guild": gld.id
        })

        new_team_id = r.json()['id']
        teams = Team.objects.all()
        assert len(teams) == 1

        new_team = Team.objects.filter(id=new_team_id).first()
        assert new_team.name == 'Team 1'
        assert new_team.guild == gld

    def test_delete_team(self):
        teams = baker.make("Team", 10)
        r = self.client.get('/api/teams/')
        data = r.json()
        assert len(data) == 10

        team_id_to_delete = teams[3].id
        self.client.delete(f'/api/teams/{team_id_to_delete}/')

        r = self.client.get('/api/teams/')
        data = r.json()
        assert len(data) == 9

        assert team_id_to_delete not in [i['id'] for i in data]

    def test_update_team(self):
        guild = baker.make('Guild', name="Blue Pegasus")
        team = baker.make('Team', name="Team 1", guild=guild)

        r = self.client.get(f'/api/teams/{team.id}/')
        data = r.json()
        assert data['name'] == team.name

        r = self.client.put(f'/api/teams/{team.id}/', {
            "name": "Team 1"
        })
        assert r.status_code == 200

        r = self.client.get(f'/api/teams/{team.id}/')
        data = r.json()
        assert data['name'] == 'Team 1'

        team.refresh_from_db()
        assert data['name'] == team.name

class GuildsViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list(self):
        r = self.client.get('/api/guilds/')
        print(r)

    def test_get_guild(self):
        guild = baker.make("Guild")

        r = self.client.get('/api/guilds/')
        data = r.json()
        print(data)

        assert guild.name == data[0]['name']
        assert guild.id == data[0]['id']
        assert len(data) == 1

    def test_create_guild(self):
        r = self.client.post("/api/guilds/", {
            "name": "Phantom Lord"
        })

        new_guild_id = r.json()['id']
        guilds = Guild.objects.all()
        assert len(guilds) == 1

        new_guild = Guild.objects.filter(id=new_guild_id).first()
        assert new_guild.name == 'Phantom Lord'

    def test_delete_guild(self):
        guilds = baker.make("Guild", 10)
        r = self.client.get('/api/guilds/')
        data = r.json()
        assert len(data) == 10

        guild_id_to_delete = guilds[3].id
        self.client.delete(f'/api/guilds/{guild_id_to_delete}/')

        r = self.client.get('/api/guilds/')
        data = r.json()
        assert len(data) == 9

        assert guild_id_to_delete not in [i['id'] for i in data]

    def test_update_guild(self):
        guilds = baker.make("Guild", 10)
        guild: Guild = guilds[2]

        r = self.client.get(f'/api/guilds/{guild.id}/')
        data = r.json()
        assert data['name'] == guild.name

        r = self.client.put(f'/api/guilds/{guild.id}/', {
            "name": "Phantom Lord"
        })
        assert r.status_code == 200

        r = self.client.get(f'/api/guilds/{guild.id}/')
        data = r.json()
        assert data['name'] == 'Phantom Lord'

        guild.refresh_from_db()
        assert data['name'] == guild.name

class CustomersViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list(self):
        r = self.client.get('/api/customers/')
        print(r)

    def test_get_customer(self):
        customer = baker.make("Customer")

        r = self.client.get('/api/customers/')
        data = r.json()
        print(data)

        assert customer.username == data[0]['username']
        assert customer.id == data[0]['id']
        assert len(data) == 1

    # def test_create_customer(self):
    #     r = self.client.post("/api/customers/", {
    #         "username": "Kaby Melon"
    #     })

    #     new_customer_id = r.json()['id']
    #     customers = Customer.objects.all()
    #     assert len(customers) == 1

    #     new_customer = Customer.objects.filter(id=new_customer_id).first()
    #     assert new_customer.username == 'Kaby Melon'

    def test_delete_customer(self):
        customers = baker.make("Customer", 10)
        r = self.client.get('/api/customers/')
        data = r.json()
        assert len(data) == 10

        customer_id_to_delete = customers[3].id
        self.client.delete(f'/api/customers/{customer_id_to_delete}/')

        r = self.client.get('/api/customers/')
        data = r.json()
        assert len(data) == 9

        assert customer_id_to_delete not in [i['id'] for i in data]

    # def test_update_customer(self):
    #     customers = baker.make("Customer", 10)
    #     customer: Customer = customers[2]

    #     r = self.client.get(f'/api/customers/{customer.id}/')
    #     data = r.json()
    #     assert data['username'] == customer.username

    #     r = self.client.put(f'/api/customers/{customer.id}/', {
    #         "username": "Kaby Melon"
    #     })
    #     assert r.status_code == 200

    #     r = self.client.get(f'/api/customers/{customer.id}/')
    #     data = r.json()
    #     assert data['username'] == 'Kaby Melon'

    #     customer.refresh_from_db()
    #     assert data['username'] == customer.username

# class OrdersViewsetTestCase(TestCase):
#     def setUp(self):
#         self.client = APIClient()

#     def test_get_list(self):
#         r = self.client.get('/api/orders/')
#         print(r)

#     def test_get_order(self):
#         gld = Guild.objects.create(
#             name="Blue Pegasus"
#         )

#         cstmr = Customer.objects.create(
#             name="Kaby Melon"
#         )
        
#         tm = Team.objects.create(
#             name="Team 1"
#         )
        
#         order = Order.objects.create(
#             name="Поиск книги отца",
#             cost="5000000",
#             status=Order.OrderStatus.NEW,
#             guild = gld,
#             customer = cstmr,
#             team=tm,
#         )

#         r = self.client.get('/api/orders/')
#         data = r.json()
#         print(data)

#         assert order.name == data[0]['name']
#         assert order.cost == data[0]['cost']
#         assert order.id == data[0]['id']
#         assert order.guild.id == data[0]['guild']
#         assert order.customer.id == data[0]['customer']
#         assert order.team.id == data[0]['team']
#         assert order.status == Order.OrderStatus.NEW.value
#         assert len(data) == 1

#     def test_create_order(self):
#         gld = baker.make("Guild")
#         cstmr = baker.make("Customer")
#         tm = baker.make("Team")

#         r = self.client.post("/api/orders/", {
#             "name": "Поиск книги отца",
#             "cost": "5000000",
#             "guild": gld.id,
#             "customer": cstmr.id,
#             "team": tm.id
#         })

#         new_order_id = r.json()['id']
#         orders = Order.objects.all()
#         assert len(orders) == 1

#         new_order = Order.objects.filter(id=new_order_id).first()
#         assert new_order.name == 'Поиск книги отца'
#         assert new_order.cost == '5000000'
#         assert new_order.guild == gld
#         assert new_order.customer == cstmr
#         assert new_order.team == tm
#         assert new_order.status == Order.OrderStatus.NEW.value

#     def test_delete_order(self):
#         orders = baker.make("Order", 10)
#         r = self.client.get('/api/orders/')
#         data = r.json()
#         assert len(data) == 10

#         order_id_to_delete = orders[3].id
#         self.client.delete(f'/api/orders/{order_id_to_delete}/')

#         r = self.client.get('/api/orders/')
#         data = r.json()
#         assert len(data) == 9

#         assert order_id_to_delete not in [i['id'] for i in data]

#     def test_update_order(self):
#         customer = baker.make('Customer', name="Kaby Melon")
#         guild = baker.make('Guild', name="Blue Pegasus")
#         team = baker.make('Team', name="Team 1")
#         order = baker.make('Order', name="Поиск книги отца", cost="5000000", status=Order.OrderStatus.NEW, customer=customer, guild=guild, team=team)

#         r = self.client.get(f'/api/orders/{order.id}/')
#         data = r.json()
#         assert data['name'] == order.name

#         new_name = "Обновленное название"
#         r = self.client.put(f'/api/orders/{order.id}/', {
#             "name": new_name,
#             "cost": "5000000",
#             "status": Order.OrderStatus.NEW.value,
#             "customer": order.customer.id,
#             "guild": order.guild.id,
#             "team": order.team.id
#         })
#         assert r.status_code == 200

#         r = self.client.get(f'/api/orders/{order.id}/')
#         data = r.json()
#         assert data['name'] == new_name

#         order.refresh_from_db()
#         assert data['name'] == order.name