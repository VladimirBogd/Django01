from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, viewsets

from wizards.models import Wizard, Guild, Order, Customer, Wizard_Order
from wizards.serializers import WizardSerializer, GuildSerializer, OrderSerializer, CustomerSerializer, Wizard_OrderSerializer

class WizardsViewset(
  mixins.CreateModelMixin,
  mixins.RetrieveModelMixin,
  mixins.UpdateModelMixin,
  mixins.DestroyModelMixin,
  mixins.ListModelMixin, 
  GenericViewSet
):
  queryset = Wizard.objects.all()
  serializer_class = WizardSerializer
#----------------------------------------------------------------------------------------------------
class GuildsViewset(
  mixins.CreateModelMixin,
  mixins.RetrieveModelMixin,
  mixins.UpdateModelMixin,
  mixins.DestroyModelMixin,
  mixins.ListModelMixin, 
  GenericViewSet
):
  queryset = Guild.objects.all()
  serializer_class = GuildSerializer
#----------------------------------------------------------------------------------------------------
class CustomersViewset(
  mixins.CreateModelMixin,
  mixins.RetrieveModelMixin,
  mixins.UpdateModelMixin,
  mixins.DestroyModelMixin,
  mixins.ListModelMixin, 
  GenericViewSet
):
  queryset = Customer.objects.all()
  serializer_class = CustomerSerializer
#----------------------------------------------------------------------------------------------------
class OrdersViewset(
  mixins.CreateModelMixin,
  mixins.RetrieveModelMixin,
  mixins.UpdateModelMixin,
  mixins.DestroyModelMixin,
  mixins.ListModelMixin, 
  GenericViewSet
):
  queryset = Order.objects.all()
  serializer_class = OrderSerializer
#----------------------------------------------------------------------------------------------------
class Wizard_OrderViewset(
  mixins.CreateModelMixin,
  mixins.RetrieveModelMixin,
  mixins.UpdateModelMixin,
  mixins.DestroyModelMixin,
  mixins.ListModelMixin, 
  GenericViewSet
):
  queryset = Wizard_Order.objects.all()
  serializer_class = Wizard_OrderSerializer