from django.urls import path
from .views import (
    RegisterChamaView,
    DetailChamaView,
    ListChamaView,
    JoinChamaView, 
    UpdateChamaView,   
    ChamaMembersView,
    CashPoolView
)
"""
    Endpoints Urls for the Chama and its Cashpool
"""
urlpatterns = [
    path('new/', RegisterChamaView.as_view(), name='register_chama'),
    path('list/', ListChamaView.as_view(), name='list_chama'),
    path('detail/<int:pk>/', DetailChamaView.as_view(), name='detail_chama'),
    path('<int:pk>/update/', UpdateChamaView.as_view(), name='update-chama'),
    path('join/', JoinChamaView.as_view(), name='join_chama'),
    path('members/<int:pk>/', ChamaMembersView.as_view(), name='chama_members'),
    path('cashpool/<int:chama_id>/', CashPoolView.as_view(), name='cashpool-detail-by-id'),
]
