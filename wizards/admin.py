from django.contrib import admin

from wizards.models import Wizard, Guild, Order, Customer, Team

# Register your models here.
@admin.register(Guild)
class GuildAdmin(admin.ModelAdmin):
  list_display = ['id', 'name']
#----------------------------------------------------------------------------------------------------
@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
  list_display = ['id', 'name', 'guild']
#----------------------------------------------------------------------------------------------------
@admin.register(Wizard)
class WizardAdmin(admin.ModelAdmin):
  list_display = ['id', 'name', 'guild', 'team']
#----------------------------------------------------------------------------------------------------
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
  list_display = ['id', 'name']
#----------------------------------------------------------------------------------------------------
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
  list_display = ['id', 'name', 'cost', 'status', 'customer', 'guild', 'team']