from django.urls import path
from .views import PayoutView, PayoutDetailView, ProcessPayoutView, PayoutCycleView

"""Url Endpoints for the Payout views"""
urlpatterns = [
    path('', PayoutView.as_view(), name='payout'),
    path('<int:pk>/', PayoutDetailView.as_view(), name='payout-detail'),
    path('<int:pk>/process/', ProcessPayoutView.as_view(), name='process-payout'),
    path('cycles/', PayoutCycleView.as_view(), name='payout-cycle')
    
]