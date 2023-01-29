from django.db import models


class ServerList(models.Model):
    server = models.CharField(max_length=16,primary_key=True)
    lockStatus = models.BooleanField()
    lastUpdate = models.DateTimeField()
    password = models.CharField(max_length=16)

class Chats(models.Model):
    chatID = models.IntegerField(primary_key=True)
    server = models.ForeignKey(ServerList,on_delete=models.CASCADE)
    username = models.CharField(max_length=16)
    message = models.CharField(max_length=256)
    time = models.DateTimeField()

class UserList(models.Model):
    userID = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=16)
    server = models.ForeignKey(ServerList,on_delete=models.CASCADE)
    time = models.DateTimeField()

