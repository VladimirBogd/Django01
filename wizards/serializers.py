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
            guild = validated_data['guild']
            new_team_instance = Team.objects.create(
                guild=guild)  # Создаем команду без имени
            # Формируем название команды с использованием id
            # Устанавливаем новое название
            new_team_instance.name = f"{new_name} (без команды)_{new_team_instance.id}"
            new_team_instance.save()  # Сохраняем изменения
            # Присваиваем экземпляр Team
            validated_data['team'] = new_team_instance
        elif "(без команды)_" in new_team.name:
            new_team.name = f"Команда {new_name}"
            new_team.save()
            validated_data['team'] = new_team
        # Создаем волшебника с обновленными данными
        return super().create(validated_data)

    def update(self, instance, validated_data):
        old_name = instance.name
        old_team = instance.team
        new_name = validated_data.get('name')
        new_team = validated_data.get('team')

        if old_team.name != f"{old_name} (без команды)_{old_team.id}":
            if old_name != new_name:
                instance.name = new_name
                if old_team != new_team:
                    # Если команда не указана, создаем новую команду
                    if new_team is None:
                        guild = validated_data.get('guild', instance.guild)
                        new_team_instance = Team.objects.create(
                            guild=guild)  # Создаем команду без имени
                        # Устанавливаем новое название
                        new_team_instance.name = f"{new_name} (без команды)_{new_team_instance.id}"
                        new_team_instance.save()  # Сохраняем изменения
                        instance.team = new_team_instance
                    elif "(без команды)_" in new_team.name:
                        new_team.name = f"Команда {new_name}"
                        new_team.save()
                        instance.team = new_team
                    else:
                        instance.team = new_team
                    if old_team.wizard_set.count() == 1:
                        old_team.delete()
            else:
                if old_team != new_team:
                    # Если команда не указана, создаем новую команду
                    if new_team is None:
                        guild = validated_data.get('guild', instance.guild)
                        new_team_instance = Team.objects.create(
                            guild=guild)  # Создаем команду без имени
                        # Устанавливаем новое название
                        new_team_instance.name = f"{new_name} (без команды)_{new_team_instance.id}"
                        new_team_instance.save()  # Сохраняем изменения
                        instance.team = new_team_instance
                    elif "(без команды)_" in new_team.name:
                        new_team.name = f"Команда {new_name}"
                        new_team.save()
                        instance.team = new_team
                    else:
                        instance.team = new_team
                    if old_team.wizard_set.count() == 1:
                        old_team.delete()
        else:
            if old_name != new_name:
                instance.name = new_name
                if new_team is None or old_team == new_team:
                    old_team.name = f"{new_name} (без команды)_{old_team.id}"
                    old_team.save()
                    instance.team = old_team
                else:
                    if "(без команды)_" in new_team.name:
                        new_team.name = f"Команда {new_name}"
                        new_team.save()
                        instance.team = new_team
                    else:
                        instance.team = new_team
                    if old_team.wizard_set.count() == 1:
                        old_team.delete()
            else:
                if new_team is None:
                    instance.team = old_team
                elif old_team != new_team:
                    if "(без команды)_" in new_team.name:
                        new_team.name = f"Команда {new_name}"
                        new_team.save()
                        instance.team = new_team
                    else:
                        instance.team = new_team
                    if old_team.wizard_set.count() == 1:
                        old_team.delete()

        # Обновляем гильдию и изображение
        instance.guild = validated_data.get('guild', instance.guild)
        instance.picture = validated_data.get('picture', instance.picture)

        instance.save()
        return instance

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
