from django.shortcuts import render
from .serializers import PayoutSerializer, ProcessPayoutSerializer, PayoutCycleSerializer, PayoutProcessResponseSerializer
from rest_framework import generics, permissions, serializers, status
from .models import Payout, PayoutCycle
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

class PayoutView(generics.ListCreateAPIView):
    serializer_class = PayoutSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Payout.objects.filter(cashpool__chama__members=self.request.user).select_related(
            'recipient', 
            'cashpool', 
            'initiated_by',
            'cashpool__chama'
        )
        status_param= self.request.query_params.get('status')

        if status_param:
            queryset = queryset.filter(status=status_param.lower())

        chama_id = self.request.query_params.get('chama_id')

        if chama_id:
            queryset = queryset.filter(cashpool__chama_id=chama_id)

        return queryset
    
    def perform_create(self, serializer):        
        serializer.save(initiated_by=self.request.user)

class PayoutDetailView(generics.RetrieveAPIView):
    queryset = Payout.objects.all()
    serializer_class = PayoutSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Payout.objects.filter(cashpool__chama__members=self.request.user)
        status_param= self.request.query_params.get('status')

        if status_param:
            queryset = queryset.filter(status=status_param.lower())

        return queryset

    def get_object(self):
        payout = get_object_or_404(
            Payout.objects.filter(
                cashpool__chama__members=self.request.user
            ),
            pk=self.kwargs['pk']
        )
        return payout

class ProcessPayoutView(generics.UpdateAPIView):
    serializer_class = ProcessPayoutSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
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
            # Check if the payout was partially processed
            if hasattr(e, 'payout'):
                response_serializer = PayoutProcessResponseSerializer(e.payout)
                return Response({
                    "status": "Payout partially processed",
                    "data": response_serializer.data,
                    "warning": str(e)
                }, status=status.HTTP_207_MULTI_STATUS)
            return Response(
                {"detail": "An unexpected error occurred"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )