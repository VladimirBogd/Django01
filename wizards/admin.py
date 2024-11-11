from django.contrib import admin

from wizards.models import Wizard, Guild, Order, Customer, Wizard_Order

# Register your models here.
@admin.register(Wizard)
class WizardAdmin(admin.ModelAdmin):
  #list_display = ['id', 'name', 'guild__id','guild']
  list_display = ['id', 'name', 'guild']
#----------------------------------------------------------------------------------------------------
@admin.register(Guild)
class GuildAdmin(admin.ModelAdmin):
  list_display = ['id', 'name']
#----------------------------------------------------------------------------------------------------
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
  list_display = ['id', 'name']
#----------------------------------------------------------------------------------------------------
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
  list_display = ['id', 'name', 'cost', 'customer', 'guild']
#----------------------------------------------------------------------------------------------------
@admin.register(Wizard_Order)
class Wizard_OrderAdmin(admin.ModelAdmin):
  list_display = ['id', 'wizard', 'order']