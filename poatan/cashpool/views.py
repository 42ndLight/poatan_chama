from django.shortcuts import render
from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import ( RegisterChamaSerializer,
                           ChamaSerializer,
                           JoinChamaSerializer,
                           ChamaMemberSerializer,
                           CashPoolSerializer 
                           )
from .models import Chama, CashPool
from rest_framework import generics

# Create your views here.
class RegisterChamaView(generics.CreateAPIView):
    queryset = Chama.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_classes = RegisterChamaSerializer

    def perform_create(self, serializer):
        serializer.save(chama_admin=self.request.user)

class DetailChamaView(generics.ListAPIView):
    queryset = Chama.objects.all()
    permission_classes  = [IsAuthenticated]
    serializer_class = ChamaSerializer

class JoinChamaView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = JoinChamaSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Successfully joined Chama!!"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_404_BAD_REQUEST)

class ChamaMembersView(generics.RetrieveAPIView):
    queryset = Chama.objects.all()
    serializer_class = ChamaMemberSerializer
    permission_classes = [IsAuthenticated]


class CashPoolView(generics.RetrieveAPIView):
    queryset = CashPool.objects.all()
    serializer_class = CashPoolSerializer
    permission_classes = [IsAuthenticated]

