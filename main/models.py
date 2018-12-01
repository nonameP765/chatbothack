from django.db import models


class Question(models.Model):
    num = models.IntegerField()
    text = models.TextField()
    isOX = models.BooleanField(default=True)

    def __str__(self):
        return str(self.num)


class Selection(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    num = models.IntegerField()
    text = models.TextField()
    taY_rank = models.IntegerField(default=0)
    taU_rank = models.IntegerField(default=0)
    soY_rank = models.IntegerField(default=0)
    soU_rank = models.IntegerField(default=0)

    def __str__(self):
        return self.text


class KakaoUser(models.Model):
    user_id = models.TextField()
    now_num = models.IntegerField(default=0)
    taY = models.IntegerField(default=0)
    taU = models.IntegerField(default=0)
    soY = models.IntegerField(default=0)
    soU = models.IntegerField(default=0)
    testMode = models.IntegerField(default=0)

    result = models.CharField(max_length=16, null=True, blank=True)

    def __str__(self):
        return self.user_id


class Constitution(models.Model):
    name = models.CharField(max_length=5)
    warning = models.TextField()
    food = models.TextField()
    prescription = models.TextField()
