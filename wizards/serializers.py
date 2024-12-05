from rest_framework import serializers

from wizards.models import Wizard, Guild, Order, Customer, Team, User

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
  
  # def update(self, instance, validated_data):
  #   instance.email = validated_data.get('email', instance.email)
  #   instance.content = validated_data.get('content', instance.content)
  #   instance.created = validated_data.get('created', instance.created)
  #   instance.save()
  #   return instance
  
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
class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'name']