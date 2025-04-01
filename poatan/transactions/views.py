from django.shortcuts import render
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import LedgerEntrySerializer, LedgerFilterSerializer
from .models import LedgerEntry

# Create your views here.
class LedgerListView(generics.ListAPIView):
    serializer_class = LedgerEntrySerializer
    filter_backends = [DjangoFilterBackend]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return LedgerFilterSerializer
        return LedgerEntrySerializer
    
    def get_querySset(self):
        queryset = LedgerEntry.objects.all()
        filter_serializer = LedgerFilterSerializer(data=self.request.query_params)
        filter_serializer.is_valid(raise_exception=True)
        filters = filter_serializer.validated_data

        if 'chama' in filters:
            queryset = queryset.filter(chama_id=filters['chama'])
        if 'user' in filters:
            queryset = queryset.filter(user_id=filters['user'])
        if 'transaction_type' in filters:
            queryset = queryset.filter(transaction_type=filters['transaction_type'])
        if 'entry_type' in filters:
            queryset = queryset.filter(entry_type=filters['entry_type'])
        if 'account' in filters:
            queryset = queryset.filter(account=filters['account'])
        if 'start_date' in filters and 'end_date' in filters:
            queryset = queryset.filter(
                timestamp__range=[filters['start_date'], filters['end_date']]
            )

        return queryset.select_related(
            'user',
            'chama',
            'initiated_by'
        ).order_by('-timestamp')