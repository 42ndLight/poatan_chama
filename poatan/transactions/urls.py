from django.urls import path
from .views import LedgerListView

urlpatterns = [
    path('', LedgerListView.as_view(), name='ledger-list'),
]