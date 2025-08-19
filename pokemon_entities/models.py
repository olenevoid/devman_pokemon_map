from django.db import models  # noqa F401

# your models here
class Pokemon(models.Model):
    name = models.CharField(max_length=200, verbose_name='Имя')
    image = models.ImageField(verbose_name='Картинка', upload_to='images/')

    def __str__(self):
        return self.name


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(
        Pokemon,
        on_delete=models.CASCADE,
        verbose_name='Покемон'
    )
    latitude = models.FloatField(verbose_name='Широта')
    longitude = models.FloatField(verbose_name='Долгота')

    def __str__(self):
        return (
            f'{self.pokemon.name} '
            f'latitude: {self.latitude} '
            f'longitude: {self.longitude} '
        )
