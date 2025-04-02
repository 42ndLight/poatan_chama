from django.shortcuts import render
from rest_framework import views, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
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

class ListChamaView(generics.ListAPIView):
    queryset = Chama.objects.all()
    permission_classes  = [IsAuthenticated]
    serializer_class = ChamaSerializer

class DetailChamaView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChamaSerializer

    def get_object(self):
        chama = get_object_or_404(
            Chama.objects.filter(
                pk=self.kwargs['pk']
            ).select_related('chama_admin', 'cash_pool')
        )
        return chama
    
class UpdateChamaView(generics.UpdateAPIView):
    queryset = Chama.objects.all()
    serializer_class = ChamaSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        chama = super().get_object()
        if chama.chama_admin != self.request.user:
            raise PermissionDenied("Only the chama admin can modify details")
        return chama
    

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


class ChamaMembersView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Chama.objects.all()
    serializer_class = ChamaMemberSerializer
    permission_classes = [IsAuthenticated]

    

class CashPoolView(generics.RetrieveAPIView):
    serializer_class = CashPoolSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        chama_id = self.kwargs.get('chama_id') or self.request.user.chama.id
        try:
            return CashPool.objects.get(chama_id=chama_id)
        except CashPool.DoesNotExist:
            return CashPool.objects.create(chama_id=chama_id)



