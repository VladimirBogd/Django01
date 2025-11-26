from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import serializers
from wizards.models import Wizard, Guild, Order, Customer, Team
from wizards.serializers import WizardSerializer, GuildSerializer, TeamSerializer, OrderSerializer, CustomerSerializer, UserSerializer
from django.db.models import Avg, Count, Max, Min


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

    def perform_create(self, serializer):
        # Здесь можно не указывать user, если он создается в сериализаторе
        serializer.save()
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
            return qs
        else:
            qs = qs.filter(user=self.request.user)
            return qs

    class StatsSerializer(serializers.Serializer):
        count = serializers.IntegerField()
        avg = serializers.FloatField()
        max = serializers.FloatField()
        min = serializers.FloatField()

    @action(detail=False, methods=["GET"], url_path="stats")
    def get_stats(self, request, *args, **kwargs):
        stats = Order.objects.aggregate(
            count=Count("*"),
            avg=Avg("cost"),
            max=Max("cost"),
            min=Min("cost"),
        )

        serializer = self.StatsSerializer(instance=stats)
        return Response(serializer.data)
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


class UserViewset(
        mixins.CreateModelMixin,
        mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
        mixins.DestroyModelMixin,
        mixins.ListModelMixin,
        GenericViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    # Новый метод для получения списка пользователей
    def list(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return Response({"error": "Недостаточно прав доступа."}, status=403)

        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(url_path="my-customers", methods=["GET"], detail=False)
    def my_customers(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"error": "Недостаточно прав доступа."}, status=403)

        customers = Customer.objects.filter(user=request.user)
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)

    @action(url_path="info", methods=["GET"], detail=False)
    def get_info(self, request, *args, **kwargs):
        data = {
            "is_authenticated": request.user.is_authenticated
        }
        if request.user.is_authenticated:
            data.update({
                "is_superuser": request.user.is_superuser,
                "username": request.user.username,
                "user_id": request.user.id,
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
