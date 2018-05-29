from django.db import models


class UserInfo(models.Model):
    """ 用户表 """

    username = models.CharField(max_length=32)
    password = models.CharField(max_length=64)
    nickname = models.CharField(max_length=32)
    roles = models.ManyToManyField('Role')

    def __str__(self):
        return self.nickname


class Permission(models.Model):
    """ 权限表 """

    title = models.CharField(max_length=32)
    url = models.CharField(max_length=64)
    menu = models.ForeignKey('Menu', null=True, blank=True)

    def __str__(self):
        return self.title


class Role(models.Model):
    """ 角色表 """

    name = models.CharField(max_length=32)
    permission = models.ManyToManyField('Permission')

    def __str__(self):
        return self.name


class Menu(models.Model):
    """ 菜单表 """

    caption = models.CharField(max_length=32)
    parent_caption = models.ForeignKey('self', null=True, blank=True)

    def __str__(self):
        return self.caption
