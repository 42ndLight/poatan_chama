from django.shortcuts import render
from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import ( 
                        RegisterChamaSerializer,
                        ChamaSerializer,
                        JoinChamaSerializer,
                        ChamaMemberSerializer,
                        CashPoolSerializer 
                           )
from .models import Chama, CashPool
from rest_framework import generics, serializers

# Create your views here.
class RegisterChamaView(generics.CreateAPIView):
    queryset = Chama.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = RegisterChamaSerializer

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
        serializer.is_valid(raise_exception=True)
        
        try:
            result = serializer.save()
            return Response({
                "message": f"Successfully joined {result['chama'].name}",
                "chama_id": result['chama'].id,
                "members_count": result['chama'].members.count()
            }, status=status.HTTP_200_OK)
        except serializers.ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ChamaMembersView(generics.RetrieveAPIView):
    queryset = Chama.objects.all()
    serializer_class = ChamaMemberSerializer
    permission_classes = [IsAuthenticated]

    

class CashPoolView(generics.RetrieveAPIView):
    serializer_class = CashPoolSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Get the chama_id from URL or user's current chama
        chama_id = self.kwargs.get('chama_id') or self.request.user.chama.id
        try:
            return CashPool.objects.get(chama_id=chama_id)
        except CashPool.DoesNotExist:
            # Auto-create if missing (redundant safety if signals work properly)
            return CashPool.objects.create(chama_id=chama_id)



