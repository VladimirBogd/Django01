from django.db import models
from django.contrib.auth.models import User

class Guild(models.Model):
  name = models.TextField("Название")
  picture = models.ImageField("Изображение", null=True, upload_to="guilds")
  
  class Meta:
    verbose_name = "Гильдия"
    verbose_name_plural = "Гильдии"

  def __str__(self) -> str:
    return self.name
#---------------------------------------------------------------------------------------------------- 
class Team(models.Model):
  name = models.TextField("Название")
  guild = models.ForeignKey("Guild", on_delete=models.CASCADE, null=True)

  class Meta:
    verbose_name = "Команда"
    verbose_name_plural = "Команды"
#----------------------------------------------------------------------------------------------------
class Wizard(models.Model):
  name = models.TextField("Имя")
  guild = models.ForeignKey("Guild", on_delete=models.CASCADE, null=True)
  team = models.ForeignKey("Team", on_delete=models.CASCADE, null=True, blank=True)
  picture = models.ImageField("Изображение", null=True, upload_to="wizards")

  class Meta:
    verbose_name = "Волшебник"
    verbose_name_plural = "Волшебники"

  def __str__(self) -> str:
    return self.name
#---------------------------------------------------------------------------------------------------- 
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)  # Связь с пользователем
    
    username = models.CharField("Название", max_length=150, null=True, blank=True)
    email = models.EmailField("Почта", null=True, blank=True)
    picture = models.ImageField("Изображение", null=True, upload_to="customers")

    class Meta:
        verbose_name = "Заказчик"
        verbose_name_plural = "Заказчики"

    def __str__(self) -> str:
        return self.user.username if self.user else "Без пользователя"
      
    def delete(self, *args, **kwargs):
        # Удаляем связанного пользователя перед удалением объекта Customer
        if self.user:
            self.user.delete()
        super().delete(*args, **kwargs)  # Вызов метода родителя для удаления Customer
#----------------------------------------------------------------------------------------------------  
class Order(models.Model):
  class OrderStatus(models.TextChoices):
    NEW = 'Новый'
    IN_PROGRESS = 'В процессе'
    COMPLETED = 'Выполнен'
    FAILED = 'Невыполнен'

  name = models.TextField("Название")
  cost = models.TextField("Стоимость")
  status = models.CharField(
      "Статус",
      max_length=20,
      choices=OrderStatus.choices,
      default=OrderStatus.NEW
  )

  customer = models.ForeignKey("Customer", on_delete=models.CASCADE, null=True)
  guild = models.ForeignKey("Guild", on_delete=models.CASCADE, null=True)
  team = models.ForeignKey("Team", on_delete=models.CASCADE, null=True, blank=True)
  
  user = models.ForeignKey("auth.User", verbose_name="Пользователь", on_delete=models.CASCADE, null=True)

  class Meta:
    verbose_name = "Заказ"
    verbose_name_plural = "Заказы"

  def __str__(self) -> str:
    return self.name