from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, viewsets
from rest_framework.decorators import action

from wizards.models import Wizard, Guild, Order, Customer, Wizard_Order
from wizards.serializers import WizardSerializer, GuildSerializer, OrderSerializer, CustomerSerializer, Wizard_OrderSerializer

from django.contrib.auth import authenticate, login

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
  #----------------------------------------------------------------------------------------------------
  class UserViewset(GenericViewSet):
    @action(url_path="info", methods=["GET"], detail=False)
    def get_info(self, request, *args, **kwargs):
      data = {
        "is_authenticated": request.user.is_authenticated 
      }
      if request.user.is_authenticated:
        data.update({
          "username": request.user.username,
          "user_id": request.user.id,
        })
      return Response(data)
    
    # @action(url_path="login", methods=["POST"], detail=False)
    # def login(self, request, *args, **kwargs):
    #   user = request.data["user"]
    #   pass = request.data["pass"]
    #   user = authenticate(request, username = user, password = pass)
    #   if user:
    #     login(request, user)
    #   return Response({})
    
    # @action(url_path = "logout", ...)
    # def logout(...)
    #   logout(request)
    #   return Response({...})