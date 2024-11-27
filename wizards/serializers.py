from rest_framework import serializers

from wizards.models import Wizard, Guild, Order, Customer, Wizard_Order, Team

class GuildSerializer(serializers.ModelSerializer):
  class Meta:
    model = Guild
    fields = ['id', 'name', 'picture']
#----------------------------------------------------------------------------------------------------
class TeamSerializer(serializers.ModelSerializer):
  class Meta:
    model = Team
    fields = ['id', 'name', 'guild']
#----------------------------------------------------------------------------------------------------
class WizardSerializer(serializers.ModelSerializer):
  guild = serializers.PrimaryKeyRelatedField(queryset=Guild.objects.all(), required=True)
  team = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all())
  class Meta:
    model = Wizard
    fields = ['id', 'name', 'guild', 'team', 'picture']
#----------------------------------------------------------------------------------------------------
class CustomerSerializer(serializers.ModelSerializer):
  class Meta:
    model = Customer
    fields = ['id', 'name', 'picture']
#----------------------------------------------------------------------------------------------------
class OrderSerializer(serializers.ModelSerializer):
  status = serializers.CharField(default=Order.OrderStatus.NEW.value)
  customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(), required=True)
  guild = serializers.PrimaryKeyRelatedField(queryset=Guild.objects.all(), required=True)
  team = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all())
  
  def create(self, validated_data): 
    if 'request' in self.context:
      validated_data['user'] = self.context['request'].user        
    return super().create(validated_data)
  
  class Meta:
    model = Order
    fields = ['id', 'name', 'cost', 'status', 'customer', 'guild', 'team', 'user']
#----------------------------------------------------------------------------------------------------
class Wizard_OrderSerializer(serializers.ModelSerializer):
  wizard = serializers.PrimaryKeyRelatedField(queryset=Wizard.objects.all(), required=True)
  order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all(), required=True)
  class Meta:
    model = Wizard_Order
    fields = ['id', 'wizard', 'order']