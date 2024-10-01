# from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Buyer_Analysis
from .serializers import BuyerAnalysisSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserCreateSerializer

class LoginView(TokenObtainPairView):
   
    pass

class BuyerAnalysisAPIView(APIView):
     
    """API View to manage buyer analysis records."""

    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    # Get all records of buyers submitted by the useer
    def get(self, request, *args, **kwargs):

        userProspects = Buyer_Analysis.objects.filter(user = request.user.id)
        serializer = BuyerAnalysisSerializer(userProspects, many = True)

        custom_data = {
            'count': userProspects.count(),
            'data': serializer.data,
            'message': 'Prospective buyers fetched successfully'
        }
        return Response(custom_data, status = status.HTTP_200_OK)
    
    # Create a new Buyer details to be analysed
    def post(self, request, *args, **kwargs):

        data = {
            'name': request.data.get('name'),
            'completed': request.data.get('completed'),
            'user': request.user.id
        }
        errors = {}
        if not data['name']:
            errors['name'] = "Name field is required."

        if not data['bank_statement']:  
            errors['bank_statement'] = "Bank statement field is required."
        
        if not data['bank_name']:
            errors['bank_name'] = "Bank name field is required."

        if errors:
            return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)

        serializer = BuyerAnalysisSerializer(data = data)
        if serializer.is_valid():
            serializer.save()

            custom_data = {
                'data': serializer.data,
                'message': 'Prospective buyer details submitted successfully'
            }
            return Response(custom_data, status = status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)



class BuyerAnalysisDetailsAPIView(APIView):

    """API View to manage details of a specific buyer analysis record."""

    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]


    # Helper method to get a specific buyer analysis object
    def get_object(self, buyer_id, user_id):

        try:
            return Buyer_Analysis.objects.get(id = buyer_id, user = user_id)
        except Buyer_Analysis.DoesNotExist:
            return None
        

   # Get specific buyer analysis 
    def get(self, request, buyer_id):

        buyer_record_instance = self.get_object(buyer_id, request.user.id)
        if not buyer_record_instance:
            return Response({"res": "record not found"}, status = status.HTTP_404_NOT_FOUND)
        
        serializer = BuyerAnalysisSerializer(buyer_record_instance)

        return Response(serializer.data, status = status.HTTP_200_OK)
    

    # Update specific buyer analysis record
    def put(self, request, buyer_id,*args, **kwargs):

        buyer_record = self.get_object(buyer_id, request.user.id)
        if not buyer_record:
            return Response({"res": "buyer record not found"}, status = status.HTTP_404_NOT_FOUND)
        
        data = {
            'name': request.data.get('name'),
            'completed': request.data.get('completed'),
            'worthy': request.data.get('worthy'),
            'user': request.user.id
        }
        serializer = BuyerAnalysisSerializer(instance = buyer_record, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

    # Delete specific buyer analysis
    def delete(self, request, buyer_id,*args, **kwargs):
        buyer_record_instance = self.get_object(buyer_id, request.user.id)
        if not buyer_record_instance:
            return Response({"res": "record not found"}, status = status.HTTP_404_NOT_FOUND)
        
        buyer_record_instance.delete()
        return Response({"res": "Object deleted!"}, status=status.HTTP_200_OK)
    

class SignupView(APIView):
    
    def post(self, request, *args, **kwargs):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)