from rest_framework.serializers import ModelSerializer, SerializerMethodField, CharField
from .models import InappropriateReason, Evaluation, Summarization

class ReasonsSerializer(ModelSerializer):
    class Meta:
        model = InappropriateReason
        exclude = ('document','id')

class SummarizationSerializer(ModelSerializer):
    file_url = SerializerMethodField()
    content = CharField(read_only=True)
    question = CharField(read_only=True)

    class Meta:
        model = Summarization
        fields = ('file_url', 'content', 'question', 'memo')
    
    def get_file_url(self, obj):
        return obj.document.file_url.url

class EvaluationSerializer(ModelSerializer):
    file_url = SerializerMethodField()

    class Meta:
        model = Evaluation
        fields = ['file_url', 'content']
    
    def get_file_url(self, obj):
        return obj.document.file_url.url