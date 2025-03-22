from django.db import models
from poatan.cashpool.models import Chama
from django.contrib.auth import get_user_model


# Create your models here.
User = get_user_model()

class Contribution(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name = "contributions")
    chama = models.ForeignKey(Chama, on_delete=models.CASCADE, related_name="contributions")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    is_confirmed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        with transaction.atomic()


    

    def __str__(self):
        return f"{self.user.username} - {self.amount}"
    

