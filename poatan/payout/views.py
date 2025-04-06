from django.shortcuts import render
from .serializers import PayoutSerializer, ProcessPayoutSerializer, PayoutCycleSerializer, PayoutProcessResponseSerializer
from rest_framework import generics, permissions, serializers, status
from .models import Payout, PayoutCycle
from django.db.models import Q
from rest_framework.exceptions import PermissionDenied
from .permissions import IsChamaAdmin
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from django.core.exceptions import PermissionDenied
import logging

logger = logging.getLogger(__name__)

# Create your views here.
class PayoutCycleView(generics.ListCreateAPIView):
    queryset = PayoutCycle.objects.all()
    serializer_class = PayoutCycleSerializer
    permission_classes = [permissions.IsAdminUser, IsChamaAdmin]

"""
    This View allows a user to create a new payout order and list them
    Its selects data based on filter such as chama_id and initiated_by in get_queryset

"""
class PayoutView(generics.ListCreateAPIView):
    serializer_class = PayoutSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Payout.objects.select_related(
            'recipient', 
            'cashpool__chama',
            'initiated_by'
        )

        # Get optional filters from query params
        status_param = self.request.query_params.get('status')
        chama_id = self.request.query_params.get('chama_id')

        # Base filter - payouts from chamas where user is a member
        queryset = queryset.filter(cashpool__chama__members=user)

        # Apply additional filters if provided
        if status_param:
            queryset = queryset.filter(status__iexact=status_param.strip())
        if chama_id:
            queryset = queryset.filter(cashpool__chama_id=chama_id)

        # If user is not admin of any relevant chama, filter further
        if not queryset.filter(cashpool__chama__chama_admin=user).exists():
            queryset = queryset.filter(
                Q(recipient=user) | 
                Q(initiated_by=user)
            )

        return queryset

    def perform_create(self, serializer):
        cashpool = serializer.validated_data['cashpool']
        user = self.request.user
        
        # Verify user is member of the chama
        if not cashpool.chama.members.filter(id=user.id).exists():
            raise PermissionDenied("You are not a member of this chama")
            
        serializer.save(initiated_by=user)

"""
    This View shows specific details on a Payout to members of his chama
"""
class PayoutDetailView(generics.RetrieveAPIView):
    serializer_class = PayoutSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Payout.objects.select_related('cashpool__chama')

    def get_object(self):
        payout = super().get_object()
        user = self.request.user
        chama = payout.cashpool.chama

        # Admin can view any payout in their chama
        if chama.chama_admin == user:
            return payout
            
        # Regular members can only view payouts they sent/received
        if user in chama.members.all() and (payout.recipient == user or payout.initiated_by == user):
            return payout
            
        raise PermissionDenied("You don't have permission to view this payout")
    
"""
    This View allows the admin to process a PAyout 
    it changes its status to confirmed and records the payoutin ledger via update method

"""
class ProcessPayoutView(generics.UpdateAPIView):
    serializer_class = ProcessPayoutSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'
    queryset = Payout.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(
            cashpool__chama__chama_admin=self.request.user
        )

    def update(self, request, *args, **kwargs):
        try:
            payout = self.get_object()
            serializer = self.get_serializer(
                payout,
                data=request.data,
                context={'request': request}
            )
            serializer.is_valid(raise_exception=True)   
            payout = serializer.save()    
            response_serializer = PayoutProcessResponseSerializer(payout)
            
            return Response({
                "status": "Payout processed successfully",
                "data": response_serializer.data
            }, status=status.HTTP_200_OK)
            
        except ValidationError as e:
            logger.error(f"Validation error processing payout: {str(e)}")
            return Response(
                {"detail": str(e.detail)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error processing payout: {str(e)}", exc_info=True)
            return Response(
                {"detail": "An unexpected error occurred"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )