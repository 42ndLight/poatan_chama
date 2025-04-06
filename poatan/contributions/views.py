from django.forms import ValidationError
from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework import status
from cashpool.models import Chama
from rest_framework.response import Response 
from rest_framework import serializers
from django.shortcuts import get_object_or_404
from .models import Contribution
from .serializers import ContributionSerializer, ConfirmContributionSerializer
import logging

logger = logging.getLogger(__name__)

"""
    View handles logic to create and list a contribution
    Only  Authenticated users can make a contribution or list their contributions
"""
class ContributionListCreateView(generics.ListCreateAPIView):
    serializer_class = ContributionSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Shows all Contributions specified to a chama
    def get_queryset(self):
        queryset = Contribution.objects.all()
        if self.kwargs.get('chama_id'):
            queryset = queryset.filter(chama_id=self.kwargs['chama_id'])
        return queryset.select_related('chama')
    
    # Ensure a Contribution is made to a specified chama
    def perform_create(self, serializer):
        chama_id = self.kwargs.get('chama_id')
        if not chama_id:
            raise serializers.ValidationError({"chama": "Chama ID is required in the URL"})
        
        try:
            chama = Chama.objects.get(pk=chama_id)
        except Chama.DoesNotExist: # Ensures the chama exists
            raise serializers.ValidationError({"chama": "Chama not found"})
        
        #Ensures only a member can view Contributions
        if not chama.members.filter(pk=self.request.user.pk).exists():
            raise PermissionDenied("You are not a member of this chama")
        
        serializer.save(user=self.request.user, chama=chama)

"""View to show specific Contribution's details """
class ContributionDetailView(generics.RetrieveAPIView):
    serializer_class = ContributionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Contribution.objects.filter(user=self.request.user)

"""
    View to show when a contribution is confrimed
    Handles:
        Only Admins can confirm a Contribution
        Only pending Contributions can be confirmed
        Proper Exception Handling when confirming a Contribution
"""
class ConfirmContributionView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ConfirmContributionSerializer
    lookup_url_kwarg = 'contribution_id'

    def get_queryset(self):
        return Contribution.objects.filter(chama__chama_admin=self.request.user)


    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(
                instance, 
                data={'status': 'confirmed'},
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            
            return Response({
                "status": "success",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
            
        except serializers.ValidationError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )