from django.db import models

# Create your models here.


from django.db import models
class UserInfo(models.Model):
    """
    用户表
    """
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=128)
    role= models.CharField(max_length=128,null=True)
# Create your models here.
class Hgroup(models.Model):
    title=models.CharField(max_length=254,verbose_name='环境',default='10套',null=False,unique=True)
    class Meta:
        verbose_name_plural = "环境表"
    def __str__(self):
        return self.title

class Host(models.Model):
    host_type_choice = (
        (0, 'windows'),
        (1, 'linux'),
    )
    ipaddr=models.CharField(max_length=254,verbose_name='IP地址',null=False)
    username=models.CharField(max_length=254,verbose_name='用户名',null=False)
    password=models.CharField(max_length=254,verbose_name='密码',null=False)
    port=models.CharField(max_length=254,verbose_name='端口',null=False)
    system_env = models.ForeignKey('Hgroup',verbose_name='环境')
    host_type = models.IntegerField(choices=host_type_choice,default=1,verbose_name='系统')

    class Meta:
        verbose_name_plural = "主机表"
    def __str__(self):
        return self.ipaddr