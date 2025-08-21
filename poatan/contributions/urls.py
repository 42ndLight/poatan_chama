from django.urls import path
from .views import ContributionListCreateView, mpesa_contribution_callback

"""Url Endpoints for the Contribution views"""
urlpatterns = [
    path('new/<int:chama_id>/', ContributionListCreateView.as_view(), name="new-contribution"),
    path('chama/<int:chama_id>/', ContributionListCreateView.as_view(), name="chama-contributions"), 
    path('callback/contributions/', mpesa_contribution_callback, name='mpesa-callback'),
    ]