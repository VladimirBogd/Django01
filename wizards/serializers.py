from rest_framework import serializers

from wizards.models import Wizard, Guild, Order, Customer, Team, User


class GuildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guild
        fields = ['id', 'name', 'picture']
# ----------------------------------------------------------------------------------------------------


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name', 'guild']
# ----------------------------------------------------------------------------------------------------


class WizardSerializer(serializers.ModelSerializer):
    guild = serializers.PrimaryKeyRelatedField(
        queryset=Guild.objects.all(), required=True)
    team = serializers.PrimaryKeyRelatedField(
        queryset=Team.objects.all(), required=False)

    def create(self, validated_data):
        new_name = validated_data.get('name')
        new_team = validated_data.get('team')

        # Если команда не указана, создаем новую команду
        if new_team is None:
            team_name = f"{new_name} (без команды)"
            guild = validated_data['guild']
            new_team_instance = Team.objects.create(name=team_name, guild=guild)
            validated_data['team'] = new_team_instance  # Присваиваем экземпляр Team

        # Если команда указана, получаем экземпляр Team
        elif isinstance(new_team, int):  # Проверяем, что это ID
            validated_data['team'] = Team.objects.get(pk=new_team)

        # Создаем волшебника с обновленными данными
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Обновляем имя и команду
        instance.name = validated_data.get('name', instance.name)
        new_team = validated_data.get('team', instance.team)

        self._handle_team_update(instance, new_team)

        # Обновляем гильдию и изображение
        instance.guild = validated_data.get('guild', instance.guild)
        instance.picture = validated_data.get('picture', instance.picture)

        instance.save()
        return instance

    def _handle_team_update(self, instance, new_team):
        old_team = instance.team

        # Проверяем, если старая команда существует и в ней больше нет волшебников
        if old_team and old_team.wizard_set.count() == 0:
            old_team.delete()

        # Если новая команда равна None, устанавливаем команду как None
        if new_team is None or new_team == "":
            instance.team = None
        else:
            # Предполагается, что new_team - это ID команды
            instance.team = Team.objects.get(id=new_team)

        # Если команда не была указана, создаем новую команду
        if instance.team is None:
            instance.team = Team.objects.create(
                name=f"{instance.name} (без команды)",
                guild=instance.guild
            )

    class Meta:
        model = Wizard
        fields = ['id', 'name', 'guild', 'team', 'picture']
# ----------------------------------------------------------------------------------------------------


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'picture']
# ----------------------------------------------------------------------------------------------------


class OrderSerializer(serializers.ModelSerializer):
    status = serializers.CharField(default=Order.OrderStatus.NEW.value)
    customer = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all(), required=True)
    guild = serializers.PrimaryKeyRelatedField(
        queryset=Guild.objects.all(), required=True)
    team = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all())

    def create(self, validated_data):
        if 'request' in self.context:
            validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    class Meta:
        model = Order
        fields = ['id', 'name', 'cost', 'status',
                  'customer', 'guild', 'team', 'user']
# ----------------------------------------------------------------------------------------------------


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name']
