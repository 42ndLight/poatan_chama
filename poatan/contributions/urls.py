from django.urls import path
from .views import ContributionListCreateView, ContributionDetailView, ConfirmContributionView

urlpatterns = [
    path('new/', ContributionListCreateView.as_view(), name="new-contribution"),
    path('', ContributionListCreateView.as_view(), name="contribution-list"), 
    path('chama/<int:chama_id>/', ContributionListCreateView.as_view(), name="chama-contributions"), 
    path('detail/<int:pk>/', ContributionDetailView.as_view(), name="detail-contribution"),
    path('confirm/<int:contribution_id>', ConfirmContributionView.as_view(), name="confirm-contribution"),
    ]