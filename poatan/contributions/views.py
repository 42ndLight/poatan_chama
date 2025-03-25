from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Contribution
from .serializers import ContributionSerializer, ConfirmContributionSerializer

class ContributionListCreateView(generics.ListCreateAPIView):
    serializer_class = ContributionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Contribution.objects.filter(user=self.request.user).select_related('chama')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ContributionDetailView(generics.RetrieveAPIView):
    serializer_class = ContributionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Contribution.objects.filter(user=self.request.user)

class ConfirmContributionView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ConfirmContributionSerializer
    queryset = Contribution.objects.all()

    def get_object(self):
        contribution = super().get_object()
        return contribution
    
    def perform_update(self, serializer):
        serializer.save(is_confirmed=True)