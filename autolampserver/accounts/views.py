from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login, get_user_model
from .serializers import UserSerializer, LoginSerializer

User = get_user_model()

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return Response({"message": "로그인 성공", "user": UserSerializer(user).data}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class UpdateDeviceIdView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        device_id = request.data.get('deviceId')
        if device_id:
            request.user.deviceId = device_id
            request.user.save()
            return Response({"message": "Device ID updated successfully"}, status=status.HTTP_200_OK)
        return Response({"error": "Device ID is required"}, status=status.HTTP_400_BAD_REQUEST)

class SequenceDataView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        datetime = request.data.get('datetime')
        class_idx = request.data.get('classIdx')
        number = request.data.get('number')

        if datetime and class_idx is not None and number is not None:
            try:
                request.user.add_sequence_data(datetime, class_idx, int(number))
                return Response({"message": "Sequence data added successfully"}, status=status.HTTP_201_CREATED)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "datetime, classIdx, and number are required"}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        sequence_data = request.user.get_sequence_data()
        return Response(sequence_data, status=status.HTTP_200_OK)