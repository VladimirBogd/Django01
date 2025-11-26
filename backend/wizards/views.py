from django.shortcuts import render
from django.http import HttpResponse
from django.views import View

from wizards.models import Wizard
from django.views.generic import TemplateView

class ShowWizardsView(TemplateView):
  template_name = "wizards/show_wizards.html"

  def get_context_data(self, **kwargs: any) -> dict[str, any]:
    context = super().get_context_data(**kwargs)
    context['wizards'] = Wizard.objects.all()

    return context