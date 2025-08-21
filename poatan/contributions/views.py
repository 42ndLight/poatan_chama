from django.db import transaction
from django.core.exceptions import PermissionDenied
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import serializers
from rest_framework.decorators import api_view, permission_classes
from django_daraja.mpesa.core import MpesaClient
from .models import Chama, Contribution
from .serializers import ContributionSerializer
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class ContributionListCreateView(generics.ListCreateAPIView):
    serializer_class = ContributionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return contributions for a specific Chama, optimized with select_related."""
        chama_id = self.kwargs.get('chama_id')
        logger.debug(f"Fetching contributions for chama_id={chama_id}, user={self.request.user.username}")
        if not chama_id:
            logger.error("Chama ID not provided in URL")
            raise serializers.ValidationError({"chama": "Chama ID is required in the URL"})
        if not Chama.objects.filter(pk=chama_id, members=self.request.user).exists():
            logger.warning(f"User {self.request.user.username} is not a member of chama_id={chama_id}")
            raise PermissionDenied("You are not a member of this chama")
        queryset = Contribution.objects.filter(chama_id=chama_id).select_related('chama', 'user')
        logger.debug(f"Queryset retrieved: {queryset.count()} contributions")
        return queryset

    def perform_create(self, serializer):
        """Create a pending contribution and initiate MPESA STK Push."""
        chama_id = self.kwargs.get('chama_id')
        logger.info(f"Creating contribution for chama_id={chama_id}, user={self.request.user.username}")
        try:
            chama = Chama.objects.get(pk=chama_id)
        except Chama.DoesNotExist:
            logger.error(f"Chama not found: chama_id={chama_id}")
            raise serializers.ValidationError({"chama": "Chama not found"})

        if not chama.members.filter(pk=self.request.user.pk).exists():
            logger.warning(f"User {self.request.user.username} is not a member of chama_id={chama_id}")
            raise PermissionDenied("You are not a member of this chama")

        with transaction.atomic():
            contribution = serializer.save(user=self.request.user, chama=chama, status='pending')
            logger.info(f"Contribution saved: ID={contribution.id}, Amount={contribution.amount}, Status={contribution.status}")

            # Initiate MPESA STK Push
            cl = MpesaClient()
            phone = self.request.user.phone_no
            amount = int(float(contribution.amount))  # Convert Decimal to int
            account_ref = f"Chama_{chama.id}"
            transaction_desc = f"Contribution to {chama.name}"
            callback_url = f"{settings.MPESA_CALLBACK_URL}contributions/"

            logger.debug(f"Initiating STK Push: phone={phone}, amount={amount}, account_ref={account_ref}, callback_url={callback_url}")
            try:
                response = cl.stk_push(
                    phone_number=phone,
                    amount=amount,
                    account_reference=account_ref,
                    transaction_desc=transaction_desc,
                    callback_url=callback_url
                )
                logger.debug(f"MPESA raw response: {response.__dict__}")
            except Exception as e:
                logger.error(f"MPESA STK Push failed: {str(e)}", exc_info=True)
                contribution.delete()
                return Response(
                    {"error": f"STK Push failed: {str(e)}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

             # Check response attributes directly
            response_code = getattr(response, 'response_code', None)
            checkout_request_id = getattr(response, 'checkout_request_id', None)
            merchant_request_id = getattr(response, 'merchant_request_id', None)
            response_description = getattr(response, 'response_description', 'Unknown error')

            if response_code == '0':
                contribution.mpesa_transaction_id = checkout_request_id
                contribution.save()
                logger.info(f"STK Push initiated: Contribution ID={contribution.id}, CheckoutRequestID={checkout_request_id}, MerchantRequestID={merchant_request_id}")
                return Response(
                    {"message": "STK Push initiated", "contribution_id": contribution.id},
                    status=status.HTTP_202_ACCEPTED
                )
            else:
                contribution.delete()
                logger.error(f"STK Push failed: {response_description}")
                return Response(
                    {"error": f"STK Push failed: {response_description}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

@api_view(['POST'])
@permission_classes([AllowAny])
def mpesa_contribution_callback(request):
    """Handle MPESA callback to update contribution status."""
    logger.info("Received MPESA callback")
    data = request.data.get('Body', {}).get('stkCallback', {})
    result_code = data.get('ResultCode')
    checkout_request_id = data.get('CheckoutRequestID')
    logger.debug(f"Callback data: ResultCode={result_code}, CheckoutRequestID={checkout_request_id}")

    if not checkout_request_id:
        logger.error("Invalid callback data: No CheckoutRequestID")
        return Response({"error": "Invalid callback data"}, status=400)

    try:
        with transaction.atomic():
            contribution = Contribution.objects.get(mpesa_transaction_id=checkout_request_id)
            logger.debug(f"Found contribution: ID={contribution.id}, Amount={contribution.amount}")
            if result_code == 0:
                contribution.status = 'confirmed'
                contribution.save()  # Triggers cashpool update via model's save
                logger.info(f"Contribution confirmed: ID={contribution.id}, Amount={contribution.amount}")
            else:
                contribution.status = 'failed'
                contribution.save()
                logger.info(f"Contribution failed: ID={contribution.id}, Reason={data.get('ResultDesc')}")
    except Contribution.DoesNotExist:
        logger.error(f"Contribution not found for CheckoutRequestID={checkout_request_id}")
        return Response({"error": "Contribution not found"}, status=404)

    return Response({"ResultCode": 0, "ResultDesc": "Callback received"})