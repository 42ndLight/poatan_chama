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

class ContributionListCreateView(generics.ListCreateAPIView):
    serializer_class = ContributionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Contribution.objects.all()
        if self.kwargs.get('chama_id'):
            queryset = queryset.filter(chama_id=self.kwargs['chama_id'])
        return queryset.select_related('chama')
    
    def perform_create(self, serializer):
        chama_id = self.kwargs.get('chama_id')
        if not chama_id:
            raise serializers.ValidationError({"chama": "Chama ID is required in the URL"})
        
        try:
            chama = Chama.objects.get(pk=chama_id)
        except Chama.DoesNotExist:
            raise serializers.ValidationError({"chama": "Chama not found"})
        
        if not chama.members.filter(pk=self.request.user.pk).exists():
            raise PermissionDenied("You are not a member of this chama")
        
        serializer.save(user=self.request.user, chama=chama)

class ContributionDetailView(generics.RetrieveAPIView):
    serializer_class = ContributionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Contribution.objects.filter(user=self.request.user)

class ConfirmContributionView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ConfirmContributionSerializer
    lookup_url_kwarg = 'contribution_id'

    def get_queryset(self):
        return Contribution.objects.filter(chama__chama_admin=self.request.user)

    def get_object(self):
        contribution = get_object_or_404(
            self.get_queryset(),
            pk=self.kwargs['contribution_id']
        )

        if contribution.is_confirmed:
            raise ValidationError({"detail": "Contribution is already confirmed"})
            
        return contribution

    def update(self, request, *args, **kwargs):
        try:
            response = super().update(request, *args, **kwargs)
            if response.status_code == status.HTTP_200_OK:
                return response
            return Response(
                {"detail": "Contribution processed successfully"},
                status=status.HTTP_200_OK
            )
        except ValidationError as e:
            if "Failed to record ledger entry" in str(e):
                contribution = self.get_object()
                if contribution.is_confirmed:
                    serializer = self.get_serializer(contribution)
                    return Response(serializer.data, status=status.HTTP_200_OK)
            logger.error(f"Validation error confirming contribution: {str(e)}")
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error confirming contribution: {str(e)}", exc_info=True)
            return Response(
                {"detail": "An unexpected error occurred"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )