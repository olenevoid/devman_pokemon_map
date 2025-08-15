from django.db import models  # noqa F401

# your models here
class Pokemon(models.Model):
    name = models.CharField(max_length=200, verbose_name='Имя')
    image = models.ImageField(verbose_name='Картинка', upload_to='images/')