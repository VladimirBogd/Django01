from django.db import models

class Guild(models.Model):
  name = models.TextField("Название")

  class Meta:
    verbose_name = "Гильдия"
    verbose_name_plural = "Гильдии"

  def __str__(self) -> str:
    return self.name
#----------------------------------------------------------------------------------------------------
class Wizard(models.Model):
  name = models.TextField("Имя")
  guild = models.ForeignKey("Guild", on_delete=models.CASCADE, null=True)

  class Meta:
    verbose_name = "Волшебник"
    verbose_name_plural = "Волшебники"

  def __str__(self) -> str:
    return self.name
#---------------------------------------------------------------------------------------------------- 
class Customer(models.Model):
  name = models.TextField("Имя")

  class Meta:
    verbose_name = "Заказчик"
    verbose_name_plural = "Заказчики"

  def __str__(self) -> str:
    return self.name
#----------------------------------------------------------------------------------------------------  
class Order(models.Model):
  name = models.TextField("Название")
  cost = models.TextField("Стоимость")

  customer = models.ForeignKey("Customer", on_delete=models.CASCADE, null=True)
  guild = models.ForeignKey("Guild", on_delete=models.CASCADE, null=True)

  class Meta:
    verbose_name = "Заказ"
    verbose_name_plural = "Заказы"

  def __str__(self) -> str:
    return self.name
#---------------------------------------------------------------------------------------------------- 
class Wizard_Order(models.Model):
  wizard = models.ForeignKey("Wizard", on_delete=models.CASCADE, null=True)
  order = models.ForeignKey("Order", on_delete=models.CASCADE, null=True)

  class Meta:
    verbose_name = "Волшебник_Заказ"
    verbose_name_plural = "Волшебник_Заказ"