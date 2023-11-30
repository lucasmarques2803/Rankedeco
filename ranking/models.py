from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class Bandeco(models.Model):
    name = models.CharField(max_length=255, default="")
    horarios = models.CharField(max_length=255, default="")
    contato = models.CharField(max_length=255, default="")
    endereco = models.CharField(max_length=255, default="")
    img_url = models.URLField(default="")

    def __str__(self):
        return f'{self.name}'


class Item(models.Model):
    name = models.CharField(max_length=255)
    bandeco = models.ManyToManyField(Bandeco, through="Nota")
    def __str__(self):
        return f'{self.name} - ({self.bandeco.name})'


class Nota(models.Model):
    bandeco = models.ForeignKey(Bandeco, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    value = models.PositiveSmallIntegerField(default=0)
    count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.bandeco} - ({self.item.name})'


class Comentario(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE)
    text = models.CharField(max_length=255, blank=True)
    bandeco = models.ForeignKey(Bandeco, on_delete=models.CASCADE)
    nota = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0, "A nota não pode ser menor que 0"), MaxValueValidator(5, "A nota não pode ser maior que 5")]
    )

    class Meta:
        ordering = ['-date',]

    def __str__(self):
        return f'{self.text} - ({self.author.username})'




