from rest_framework import serializers

from wizards.models import Wizard, Guild, Order, Customer, Wizard_Order

class GuildSerializer(serializers.ModelSerializer):
  class Meta:
    model = Guild
    fields = ['id', 'name', 'picture']
#----------------------------------------------------------------------------------------------------
class CustomerSerializer(serializers.ModelSerializer):
  class Meta:
    model = Customer
    fields = ['id', 'name', 'picture']
#----------------------------------------------------------------------------------------------------
class WizardSerializer(serializers.ModelSerializer):
  # guild = GuildSerializer(read_only=True)
  class Meta:
    model = Wizard
    fields = ['id', 'name', 'guild', 'picture']
#----------------------------------------------------------------------------------------------------
class OrderSerializer(serializers.ModelSerializer):
  # guild = GuildSerializer(read_only=True)
  # customer = CustomerSerializer(read_only=True)
  class Meta:
    model = Order
    fields = ['id', 'name', 'cost', 'customer', 'guild']
#----------------------------------------------------------------------------------------------------
class Wizard_OrderSerializer(serializers.ModelSerializer):
  # wizard = WizardSerializer(read_only=True)
  # order = OrderSerializer(read_only=True)
  class Meta:
    model = Wizard_Order
    fields = ['id', 'wizard', 'order']