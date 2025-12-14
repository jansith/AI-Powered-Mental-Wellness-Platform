from django.shortcuts import render
from rest_framework.views import APIView,status
from .models import *
from .serializer import *
from rest_framework.response import Response

class ADHDQuestionnaireApi(APIView):

    def post(self, request):
        serializer = ADHDQuestionnaireSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response({
                'status': 'success',
                'message': 'ADHD Question answers created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'status': 'error',
            'message': 'ADHD Question answers creation failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, id=None):
        try:
            if id is not None:
                adhq_result = ADHDQuestionnaire.objects.get(user=id)
                serializer = ADHDQuestionnaireSerializer(adhq_result)
                return Response({
                    'status': 'success',
                    'message': 'ADHD result data retrieved successfully',
                    'data': serializer.data,
                    'count': serializer.data
                }, status=status.HTTP_200_OK)
        
            adhq_result = ADHDQuestionnaire.objects.all()
            serializer = ADHDQuestionnaireSerializer(adhq_result, many=True)
            return Response({
                'status': 'success',
                'message': 'ADHD result data retrieved successfully',
                'data': serializer.data,
                'count': len(serializer.data)
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({
                'status': 'error',
                'message': 'Failed to retrieve ADHD result data',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


class DepressionQuestionnaireApi(APIView):

    def post(self, request):
        serializer = DepressionQuestionnaireSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response({
                'status': 'success',
                'message': 'Depression Question answers created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'status': 'error',
            'message': 'Depression Question answers creation failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, id=None):
        try:
            if id is not None:
                depression_result = DepressionQuestionnaire.objects.get(user=id)
                serializer = DepressionQuestionnaireSerializer(depression_result)
                return Response({
                    'status': 'success',
                    'message': 'Depression result data retrieved successfully',
                    'data': serializer.data,
                    'count': serializer.data
                }, status=status.HTTP_200_OK)
            
            depression_result = DepressionQuestionnaire.objects.all()
            serializer = DepressionQuestionnaireSerializer(depression_result, many=True)
            return Response({
                'status': 'success',
                'message': 'Depression result data retrieved successfully',
                'data': serializer.data,
                'count': len(serializer.data)
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({
                'status': 'error',
                'message': 'Failed to retrieve depression result data',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)