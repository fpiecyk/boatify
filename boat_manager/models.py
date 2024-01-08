from django.db import models
from django.contrib.auth.models import User, AbstractUser


# Create your models here.
class Pier(models.Model):
    name = models.CharField(max_length=25)
    address = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Boat(models.Model):
    pier_id = models.ForeignKey(Pier, on_delete=models.PROTECT)
    type = models.CharField(max_length=15)
    name = models.CharField(max_length=25)
    length = models.CharField(max_length=15)
    capacity = models.CharField(max_length=5)
    engine_power = models.CharField(max_length=5)
    description = models.TextField(max_length=300)
    image = models.ImageField(null=True, blank=True)
    daily_price = models.IntegerField()

    def __str__(self):
        return f"{self.type} | {self.name} | {self.length} | {self.capacity} | {self.daily_price}"


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=12, blank=True)
    wallet = models.IntegerField(default = 0)


class Bookings(models.Model):
    boat_id = models.ForeignKey(Boat, on_delete=models.PROTECT)
    customer_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    total_price = models.IntegerField(null=True, blank=True)
    booking_confirm = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Bookings"

    def __str__(self):
        return (f"Łódź {self.boat_id.name} została zarezerwowana od {self.start_date} do {self.end_date}. "
                f"| Kwota całkowita {self.total_price} PLN.")




