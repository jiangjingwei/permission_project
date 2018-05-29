from django.forms import ModelForm
from . import models


class UserModel(ModelForm):
    class Meta:
        model = models.UserInfo
        fields = "__all__"
