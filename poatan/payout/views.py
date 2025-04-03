from django.shortcuts import render
from .serializers import PayoutSerializer, ProcessPayoutSerializer, PayoutCycleSerializer
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
                context={'payout': payout, 'request': request}
            )
            serializer.is_valid(raise_exception=True)
            
            response = super().update(request, *args, **kwargs)
            
            if response.status_code == status.HTTP_200_OK:
                return Response(
                    {
                        "status": "Payout processed successfully",
                        "data": response.data
                    },
                    status=status.HTTP_200_OK
                )
            
            return Response(
                {"detail": "Payout processed successfully"},
                status=status.HTTP_200_OK
            )
            
        except ValidationError as e:
            if "Failed to record ledger entry" in str(e):
                # Check if payout was actually processed
                payout.refresh_from_db()
                if payout.status == 'completed':
                    serializer = self.get_serializer(payout)
                    return Response(
                        {
                            "status": "Payout already processed",
                            "data": serializer.data
                        },
                        status=status.HTTP_200_OK
                    )
            
            logger.error(f"Validation error processing payout: {str(e)}")
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        except PermissionDenied as e:
            logger.error(f"Permission denied processing payout: {str(e)}")
            return Response(
                {"detail": str(e)},
                status=status.HTTP_403_FORBIDDEN
            )
            
        except Exception as e:
            logger.error(f"Error processing payout: {str(e)}", exc_info=True)
            return Response(
                {"detail": "An unexpected error occurred"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        