from django.urls import path
from .views import PayoutView, PayoutDetailView, ProcessPayoutView


urlpatterns = [
    path('', PayoutView.as_view(), name='payout-list'),
     path('new/', PayoutView.as_view(), name='payout-create'),
    path('<int:pk>/', PayoutDetailView.as_view(), name='payout-detail'),
    path('<int:pk>/process/', ProcessPayoutView.as_view(), name='process-payout'),
]