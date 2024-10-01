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
import camelot
import pandas as pd

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
        # Handling the uploaded bank statement PDF file
        statement = request.FILES.get('bank_statement')

        if not statement:
            return Response({"errors": "Bank statement field is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Save the uploaded file temporarily to process with Camelot
        temp_file_path = '/tmp/' + statement.name
        with open(temp_file_path, 'wb+') as temp_file:
            for chunk in statement.chunks():
                temp_file.write(chunk)

        try:
            # Camelot processing on the temporary file
            tables = camelot.read_pdf(temp_file_path)
            print(f"Total tables found: {tables.n}")
            first_table = tables[0].df
            second_table = tables[1].df
            print(first_table, second_table)

            # begin analysis with pandas
            df = pd.DataFrame(second_table)

            # prints out few lines from the table
            print(df.head())

            # Example analysis: assuming columns 0, 1 are Date and Amount
            df.columns = ['Date', 'Description', 'Amount']  # Adjust based on actual table structure
            df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')  # Convert Amount column to numeric
            
            # Drop any rows where Amount is NaN
            df_cleaned = df.dropna(subset=['Amount'])
            
            # Calculate some basic statistics
            total_amount = df_cleaned['Amount'].sum()
            average_amount = df_cleaned['Amount'].mean()
            num_transactions = df_cleaned.shape[0]

            analysis_results = {
                'total_amount': total_amount,
                'average_amount': average_amount,
                'num_transactions': num_transactions
            }
            # decision willl nw be made wether this passes the test or not and if the user is worthy
        
           

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
             

        # Proceed with the rest of the data extraction and processing
        data = {
            'name': request.data.get('name'),
            'completed': request.data.get('completed'),
            'bank_statement': temp_file_path,  # will probbly upload it or something for reference purpose
            'bank_name': request.data.get('bank_name'),
            'user': request.user.id
        }

        serializer = BuyerAnalysisSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data, "message": "Prospective buyer details submitted successfully"}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
        



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