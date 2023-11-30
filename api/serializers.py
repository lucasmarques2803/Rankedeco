from rest_framework import serializers

from ranking.models import Nota, Bandeco, Comentario, Item

class ComentarioSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comentario
        fields = ['id', 'date', 'author', 'text', 'bandeco', 'nota']

class BandecoSerializer(serializers.ModelSerializer):
    comentario_set = ComentarioSerializer(many=True, read_only=True)

    class Meta:
        model = Bandeco
        fields = ['id', 'name', 'horarios', 'contato', 'endereco', 'img_url', 'comentario_set']

class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = ['id', 'name']

class NotaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Nota
        fields = ['id', 'bandeco', 'item', 'value', 'count']






