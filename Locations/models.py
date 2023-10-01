from django.db import models
import uuid

class Locations(models.Model):
    locaion_id = models.UUIDField(
        default=uuid.uuid4, 
        db_index=True, 
        editable=False, 
        primary_key=True, 
        unique=True
        )
    house_number = models.CharField(max_length=15, default='-') # เลขที่บ้าน
    section = models.CharField(max_length=10, default='-') # หมู่บ้าน
    street = models.CharField(max_length=15, default='-') # ถนน
    sub_district = models.CharField(max_length=30, default='-') # ตำบล
    district = models.CharField(max_length=30, default='-') # อำเภอ
    province = models.CharField(max_length=30, default='-') # จังหวัด
    postcode = models.CharField(max_length=10, default='-')
    country = models.CharField(max_length=30, default="Thailand")
    latitude = models.FloatField(max_length=15, default=0)
    longtitude = models.FloatField(max_length=15, default=0)
    
    def __str__(self) -> str:
        data = self.__dict__.items()
        result = ''
        for key, value in data:
            if key not in ['latitude', 'longtitude']:
                result += f'{value}'
        return result
