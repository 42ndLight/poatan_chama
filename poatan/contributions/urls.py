from django.urls import path
from .views import ContributionListCreateView, ContributionDetailView, ConfirmContributionView

"""Url Endpoints for the Contribution views"""
urlpatterns = [
    path('<int:chama_id>/new/', ContributionListCreateView.as_view(), name="new-contribution"),
    path('chama/<int:chama_id>/', ContributionListCreateView.as_view(), name="chama-contributions"), 
    path('detail/<int:pk>/', ContributionDetailView.as_view(), name="detail-contribution"),
    path('confirm/<int:contribution_id>/', ConfirmContributionView.as_view(), name="confirm-contribution"),
    ]