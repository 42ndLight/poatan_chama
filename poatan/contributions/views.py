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
        return Contribution.objects.filter(user=self.request.user)

class ContributionDetailView(generics.RetrieveAPIView):
    queryset = Contribution.objects.all()
    serializer_class = ContributionSerializer
    permission_classes = [permissions.IsAuthenticated]

class ConfirmContributionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, contribution_id):
        try:
            contribution = Contribution.objects.get(id=contribution_id, user=request.user)
        except Contribution.DoesNotExist:
            return Response({"error": "Contribution not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ConfirmContributionSerializer(contribution, data={"is_confirmed": True}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Contribution confirmed"}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
