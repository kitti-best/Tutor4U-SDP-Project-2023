from django.db import models
import uuid

class Locations(models.Model):
    location_id = models.UUIDField(
        default=uuid.uuid4, 
        db_index=True, 
        editable=False, 
        primary_key=True, 
        unique=True
        )
    house_number = models.CharField(max_length=50, default='-', blank=True) # เลขที่บ้าน
    section = models.CharField(max_length=150, default='-', blank=True) # หมู่บ้าน
    street = models.CharField(max_length=150, default='-', blank=True) # ถนน
    sub_district = models.CharField(max_length=150, default='-') # ตำบล
    district = models.CharField(max_length=150, default='-') # อำเภอ
    province = models.CharField(max_length=150, default='-') # จังหวัด
    postcode = models.CharField(max_length=10, default='-')
    country = models.CharField(max_length=50, default="ประเทศไทย")
    latitude = models.FloatField(max_length=15, default=0)
    longitude = models.FloatField(max_length=15, default=0)
    
    def __str__(self) -> str:
        data = self.__dict__.items()
        result = ''
        for key, value in data:
            if key not in ['latitude', 'longtitude']:
                result += f'{value}'
        return result
