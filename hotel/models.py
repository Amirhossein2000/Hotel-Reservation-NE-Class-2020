from django.db import models


# Create your models here.

class Room(models.Model):
    room_number = models.IntegerField(db_column='room_id', primary_key=True)  # Field name made lowercase.
    beds_count = models.IntegerField(db_column='beds_count')
    floor_number = models.IntegerField(db_column='floor_number')
    amount = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        managed = True
        db_table = 'room'


class Service(models.Model):
    service_id = models.AutoField(db_column='service_id', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='name', max_length=200)
    Description = models.TextField(db_column='description', null=True)
    amount = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        managed = True
        db_table = 'service'


class Customer(models.Model):
    name = models.CharField(db_column='name', max_length=200)
    email = models.EmailField()

    class Meta:
        managed = True
        db_table = 'customer'


class Reservation(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)  # Field name made lowercase.
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    services = models.ManyToManyField(Service)
    start_time = models.DateField()
    end_time = models.DateField()
    amount = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        managed = True
        db_table = 'reservation'
