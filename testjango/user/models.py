# user/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
# project 폴더의 settings가 맞다
# 장고가 설정해주도록 django로 가져옴
from django.conf import settings


# AbstractUser(장고의 기본 제공하는 기능)을 UserMode안에서 사용
class UserModel(AbstractUser):
    # DB 테이블의 이름을 지정해주는 정보
    # 데이터베이스에 정보를 넣어주는 역할
    class Meta:
        # 'my_user'는 db table 이름
        db_table = "my_user"

    # CharField, DateTimeField 어떤 형태로 DB에 들어갈지 설정
    # AbstractUser 기능외에 bio 기능을 추가
    bio = models.CharField(max_length=256, default='')
    # follow : 사용자 정보, 사용자가 사용자 모델을 팔로우
    # 내가 팔로우한 사람 변수 follow
    # 유명인 입장에서는 내가 followee
    # UserModel.followee : 유저 모델(유명인)을 팔로우하는 사람들을 불러 줌
    # UserModel.follow : 내가 팔로우하는 사람을 불러 줌
    follow = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='followee')
