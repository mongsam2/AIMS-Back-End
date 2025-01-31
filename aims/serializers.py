from rest_framework.serializers import ModelSerializer, SerializerMethodField, CharField
from .models import DocumentPassFail, Evaluation, Summarization, EssayCriteria, EvaluationRange


class DocumentPassFailSerializer(ModelSerializer):
    class Meta:
        model = DocumentPassFail
        exclude = ('document_id','id')


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
        fields = ['file_url', 'content', 'memo']
    
    def get_file_url(self, obj):
        return obj.document.file_url.url


class EvaluationRangeSerializer(ModelSerializer):
    class Meta:
        model = EvaluationRange
        fields = '__all__'


class EssayCriteriaSerializer(ModelSerializer):
    ranges = EvaluationRangeSerializer(many=True)

    class Meta:
        model = EssayCriteria
        exclude = ('id',)


