from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from authentication.utils import generate_otp, verify_otp
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import re
import json

User = get_user_model()
@csrf_exempt
def register(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            email = data.get('email')
            regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
            if(not re.fullmatch(regex, email)):
                return JsonResponse({"message": "Invalid Email address"}, status=406)
            if User.objects.filter(email=email).exists():
                return JsonResponse({'message': 'Email already registered'}, status=400)
            user = User.objects.create_user(username=email, email=email)
            return JsonResponse({'message': 'Registration successful. Please verify your email.'})
        else:
            return JsonResponse({'message': 'Method not allowed'}, status=405)
    except Exception as err:
        return JsonResponse({"error": err}, status=500)

@csrf_exempt
def request_otp(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            print(f"This is Data: {data}")
            email = data.get('email')
            print(f"email {email}")
            if not email:
                return JsonResponse({"message": "No input found"}, status=400)
            user = User.objects.filter(email=email).first()
            if user:
                otp = generate_otp(user)
                return JsonResponse({'message': 'OTP sent to your email.'})
            return JsonResponse({'message': 'User not found'}, status=404)
        else:
            return JsonResponse({'message': 'Method not allowed'}, status=405)
    except Exception as err:
        return JsonResponse({"error": str(err)}, status=500)


@csrf_exempt
def verify_otp_view(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            email = data.get('email')
            otp = data.get('otp')
            user = User.objects.filter(email=email).first()
            if user and verify_otp(user, otp):
                login(request, user)
                refresh = RefreshToken.for_user(user)
                return JsonResponse({
                    'message': 'Login successful.',
                    'access_token': str(refresh.access_token),
                    'refresh_token': str(refresh)
                })
            return JsonResponse({'message': 'Invalid OTP'}, status=400)
        else:
            return JsonResponse({'message': 'Method not allowed'}, status=405)
    except Exception as err:
        return JsonResponse({"error": str(err)}, status=500)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_view(request):
    return Response({"message": "This is a protected route", "user": request.user.email})