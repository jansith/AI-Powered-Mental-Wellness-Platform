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