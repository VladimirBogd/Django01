from django.test import TestCase
from rest_framework.test import APIClient
from model_bakery import baker

from wizards.models import Wizard, Guild, Order, Customer, Wizard_Order

# Create your tests here.
class WizardsViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list(self):
        r = self.client.get('/api/wizards/')
        print(r)

    def test_get_wizard(self):
        gld = Guild.objects.create(
            name="Blue Pegasus"
        )
        
        wizard = Wizard.objects.create(
            name="Hibiki Lates",
            guild = gld,
        )

        r = self.client.get('/api/wizards/')
        data = r.json()
        print(data)

        assert wizard.name == data[0]['name']
        assert wizard.id == data[0]['id']
        assert wizard.guild.id == data[0]['guild']
        assert len(data) == 1

    def test_create_wizard(self):
        gld = baker.make("wizards.Guild")

        r = self.client.post("/api/wizards/", {
            "name": "Hibiki Lates",
            "guild": gld.id
        })

        new_wizard_id = r.json()['id']
        wizards = Wizard.objects.all()
        assert len(wizards) == 1

        new_wizard = Wizard.objects.filter(id=new_wizard_id).first()
        assert new_wizard.name == 'Hibiki Lates'
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
        wizards = baker.make("Wizard", 10)
        wizard: Wizard = wizards[2]

        r = self.client.get(f'/api/wizards/{wizard.id}/')
        data = r.json()
        assert data['name'] == wizard.name

        r = self.client.put(f'/api/wizards/{wizard.id}/', {
            "name": "Laxus Dreyar"
        })
        assert r.status_code == 200

        r = self.client.get(f'/api/wizards/{wizard.id}/')
        data = r.json()
        assert data['name'] == 'Laxus Dreyar'

        wizard.refresh_from_db()
        assert data['name'] == wizard.name

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

        assert customer.name == data[0]['name']
        assert customer.id == data[0]['id']
        assert len(data) == 1

    def test_create_customer(self):
        r = self.client.post("/api/customers/", {
            "name": "Kaby Melon"
        })

        new_customer_id = r.json()['id']
        customers = Customer.objects.all()
        assert len(customers) == 1

        new_customer = Customer.objects.filter(id=new_customer_id).first()
        assert new_customer.name == 'Kaby Melon'

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

    def test_update_customer(self):
        customers = baker.make("Customer", 10)
        customer: Customer = customers[2]

        r = self.client.get(f'/api/customers/{customer.id}/')
        data = r.json()
        assert data['name'] == customer.name

        r = self.client.put(f'/api/customers/{customer.id}/', {
            "name": "Kaby Melon"
        })
        assert r.status_code == 200

        r = self.client.get(f'/api/customers/{customer.id}/')
        data = r.json()
        assert data['name'] == 'Kaby Melon'

        customer.refresh_from_db()
        assert data['name'] == customer.name

class OrdersViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list(self):
        r = self.client.get('/api/orders/')
        print(r)

    def test_get_order(self):
        gld = Guild.objects.create(
            name="Blue Pegasus"
        )

        cstmr = Customer.objects.create(
            name="Kaby Melon"
        )
        
        order = Order.objects.create(
            name="Поиск книги отца",
            cost="5000000",
            guild = gld,
            customer = cstmr
        )

        r = self.client.get('/api/orders/')
        data = r.json()
        print(data)

        assert order.name == data[0]['name']
        assert order.cost == data[0]['cost']
        assert order.id == data[0]['id']
        assert order.guild.id == data[0]['guild']
        assert order.customer.id == data[0]['customer']
        assert len(data) == 1

    def test_create_order(self):
        gld = baker.make("Guild")
        cstmr = baker.make("Customer")

        r = self.client.post("/api/orders/", {
            "name": "Поиск книги отца",
            "cost": "5000000",
            "guild": gld.id,
            "customer": cstmr.id
        })

        new_order_id = r.json()['id']
        orders = Order.objects.all()
        assert len(orders) == 1

        new_order = Order.objects.filter(id=new_order_id).first()
        assert new_order.name == 'Поиск книги отца'
        assert new_order.cost == '5000000'
        assert new_order.guild == gld
        assert new_order.customer == cstmr

    def test_delete_order(self):
        orders = baker.make("Order", 10)
        r = self.client.get('/api/orders/')
        data = r.json()
        assert len(data) == 10

        order_id_to_delete = orders[3].id
        self.client.delete(f'/api/orders/{order_id_to_delete}/')

        r = self.client.get('/api/orders/')
        data = r.json()
        assert len(data) == 9

        assert order_id_to_delete not in [i['id'] for i in data]

    def test_update_order(self):
        orders = baker.make("Order", 10)
        order: Order = orders[2]

        r = self.client.get(f'/api/orders/{order.id}/')
        data = r.json()
        assert data['name'] == order.name

        r = self.client.put(f'/api/orders/{order.id}/', {
            "name": "Поиск книги отца",
            "cost": "5000000"
        })
        assert r.status_code == 200

        r = self.client.get(f'/api/orders/{order.id}/')
        data = r.json()
        assert data['name'] == 'Поиск книги отца'

        order.refresh_from_db()
        assert data['name'] == order.name

class Wizard_Wizard_OrderViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list(self):
        r = self.client.get('/api/wizard_order/')
        print(r)

    def test_get_wizard_order(self):
        gld = Guild.objects.create(
            name="Blue Pegasus"
        )
        
        wzrd = Wizard.objects.create(
            name="Lucy Heartfilia",
            guild=gld
        )

        cstmr = Customer.objects.create(
            name="Kaby Melon"
        )

        ordr = Order.objects.create(
            name="Поиск книги отца",
            cost="5000000",
            guild = gld,
            customer = cstmr
        )
        
        wizard_order = Wizard_Order.objects.create(
            wizard = wzrd,
            order = ordr
        )

        r = self.client.get('/api/wizard_order/')
        data = r.json()
        print(data)

        assert wizard_order.wizard.id == data[0]['wizard']
        assert wizard_order.order.id == data[0]['order']
        assert len(data) == 1

    def test_create_wizard_order(self):
        wzrd = baker.make("Wizard")
        ordr = baker.make("Order")

        r = self.client.post("/api/wizard_order/", {
            "wizard": wzrd.id,
            "order": ordr.id
        })

        new_wizard_order_id = r.json()['id']
        wizard_orders = Wizard_Order.objects.all()
        assert len(wizard_orders) == 1

        new_wizard_order = Wizard_Order.objects.filter(id=new_wizard_order_id).first()
        assert new_wizard_order.wizard == wzrd
        assert new_wizard_order.order == ordr

    def test_delete_wizard_order(self):
        wizard_orders = baker.make("Wizard_Order", 10)
        r = self.client.get('/api/wizard_order/')
        data = r.json()
        assert len(data) == 10

        wizard_order_id_to_delete = wizard_orders[3].id
        self.client.delete(f'/api/wizard_order/{wizard_order_id_to_delete}/')

        r = self.client.get('/api/wizard_order/')
        data = r.json()
        assert len(data) == 9

        assert wizard_order_id_to_delete not in [i['id'] for i in data]