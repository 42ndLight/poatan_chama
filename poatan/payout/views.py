from django.shortcuts import render
from .serializers import PayoutSerializer, ProcessPayoutSerializer
from rest_framework import generics, permissions, status
from .models import Payout
from rest_framework.exceptions import PermissionDenied
from cashpool.models import Chama
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

# Create your views here.
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
        chama = serializer.validated_data['cashpool'].chama

        if not chama.admin == self.request.user:
            raise PermissionDenied("Only Chama admins can initiate payouts")
        
        serializer.save(initiated_by=self.request.user)

class PayoutDetailView(generics.RetrieveAPIView):
    queryset = Payout.objects.all()
    serializer_class = PayoutSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        payout = get_object_or_404(
            Payout.objects.filter(
                cashpool__chama__members=self.request.user
            ),
            pk=self.kwargs['pk']
        )
        return payout

class ProcessPayoutView(generics.UpdateAPIView):
    queryset = Payout.objects.all()
    serializer_class = ProcessPayoutSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        payout = get_object_or_404(
            Payout.objects.filter(
                cashpool__chama__admin=self.request.user
            ),
            pk=self.kwargs['pk']
        )
        return payout

    
    def update(self, request, *args, **kwargs):
        payout = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        action = serializer.validated_data['action']

        if action == 'approve':
            try:
                success = payout.process()
                if success:
                    return Response(
                        {"detail": "Payout processed successfully"},
                        status=status.HTTP_200_OK
                    )
                return Response(
                    {"detail": "Payout processing failed"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            except Exception as e:
                return Response(
                    {"detail": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        else:
            payout.status = 'failed'
            payout.failure_reason = serializer.validated_data.get('reason', 'Denied by admin')
            payout.save()
            return Response(
                {"detail": "Payout rejected"},
                status=status.HTTP_200_OK
            )
