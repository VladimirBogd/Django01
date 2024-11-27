"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static

from wizards import views
from rest_framework.routers import DefaultRouter

from wizards.api import WizardsViewset, GuildsViewset, TeamsViewset, CustomersViewset, OrdersViewset, OrderStatusViewset, UserViewset

router = DefaultRouter()
router.register("wizards", WizardsViewset, basename="wizards")
router.register("guilds", GuildsViewset, basename="guilds")
router.register("teams", TeamsViewset, basename="teams")
router.register("customers", CustomersViewset, basename="customers")
router.register("orders", OrdersViewset, basename="orders")
router.register("users", UserViewset, basename="user")
router.register("order-statuses", OrderStatusViewset, basename="order-statuses")

urlpatterns = [
    path('', views.ShowWizardsView.as_view()),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
