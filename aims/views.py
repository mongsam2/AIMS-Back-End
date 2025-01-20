from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Extraction, Summarization, InappropriateReason, Evaluation  


# Create your views here.
class ExtractionView(APIView):
    def post(self, request, document_id):

        
        return Response({'message': '딕셔너리 형태로 응답'})
    
class SummarizationView(APIView):
    def post(self, request, document_id):


        return Response({'message': '딕셔너리 형태로 응답'})

class ReasonView(APIView):
    def post(self, request, document_id):


        return Response({'message': '딕셔너리 형태로 응답'})

class EvaluationView(APIView):
    def post(self, request, document_id):


        return Response({'message': '딕셔너리 형태로 응답'})