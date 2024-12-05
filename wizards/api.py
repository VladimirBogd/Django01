from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework.response import Response
from wizards.models import Wizard, Guild, Order, Customer, Team
from wizards.serializers import WizardSerializer, GuildSerializer, TeamSerializer, OrderSerializer, CustomerSerializer

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
# ----------------------------------------------------------------------------------------------------


class TeamsViewset(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
# ----------------------------------------------------------------------------------------------------


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
# ----------------------------------------------------------------------------------------------------


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
# ----------------------------------------------------------------------------------------------------


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

    def get_queryset(self):
        qs = super().get_queryset()
        # фильтруем по текущему юзеру
        if (self.request.user.is_superuser):
            qs = qs.filter(user=self.request.user)
            return qs
# ----------------------------------------------------------------------------------------------------


class OrderStatusViewset(viewsets.ViewSet):
    def list(self, request):
        statuses = [
            {'id': 'Новый', 'name': 'Новый'},
            {'id': 'В процессе', 'name': 'В процессе'},
            {'id': 'Выполнен', 'name': 'Выполнен'},
            {'id': 'Невыполнен', 'name': 'Невыполнен'},
        ]
        return Response(statuses)
# ----------------------------------------------------------------------------------------------------


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
                "is_superuser": request.user.is_superuser,
            })
        return Response(data)

    @action(url_path="login", methods=["POST"], detail=False)
    def login(self, request, *args, **kwargs):
        username = request.data.get("user")
        password = request.data.get("pass")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return Response({"success": True})
        return Response({"success": False, "error": "Invalid credentials"}, status=400)

    @action(url_path="logout", methods=["GET"], detail=False)
    def logout(self, request, *args, **kwargs):
        logout(request)
        return Response({"success": True})
