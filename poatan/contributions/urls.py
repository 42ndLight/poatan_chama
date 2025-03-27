from django.urls import path
from .views import ContributionListCreateView, ContributionDetailView, ConfirmContributionView

urlpatterns = [
    path('new/', ContributionListCreateView.as_view(), name="new-contribution"),
    path('list/<int:chama_id>', ContributionListCreateView.as_view(), name="list-contribution"),
    path('detail/<int:contribution_id>/', ContributionDetailView.as_view(), name="detail-contribution"),
    path('confirm/<int:contribution_id>', ConfirmContributionView.as_view(), name="confirm-contribution"),
    ]