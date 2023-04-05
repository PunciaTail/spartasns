from django.contrib import admin
#.models admin.py 위치와 동일한 위치의 models 파일의 UserModel을 불러옴
from .models import UserModel

# Register your models here.
admin.site.register(UserModel) # 이 코드가 나의 UserModel을 Admin에 추가 해 줍니다