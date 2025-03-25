from django.urls import path
from .views import (
    RegisterChamaView,
    DetailChamaView,
    JoinChamaView,    
    ChamaMembersView,
    CashPoolView
)

urlpatterns = [
    path('new/', RegisterChamaView.as_view(), name='register_chama'),
    path('detail/', DetailChamaView.as_view(), name='detail_chama'),
    path('join/', JoinChamaView.as_view(), name='join_chama'),
    path('members/<int:pk>/', ChamaMembersView.as_view(), name='chama_members'),
    path('cashpool/<int:chama_id>/', CashPoolView.as_view(), name='cashpool-detail-by-id'),
]
