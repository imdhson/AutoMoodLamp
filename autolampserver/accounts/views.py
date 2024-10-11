from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import authenticate, get_user_model, logout
from .serializers import UserSerializer, LoginSerializer
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

User = get_user_model()

@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "user": UserSerializer(user).data,
                "token": token.key
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    "message": "로그인 성공",
                    "user": UserSerializer(user).data,
                    "token": token.key
                }, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

@method_decorator(csrf_exempt, name='dispatch')
class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # 토큰 삭제
        request.user.auth_token.delete()
        # Django 세션 로그아웃 (세션 기반 인증을 사용하는 경우)
        logout(request)
        return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)

@method_decorator(csrf_exempt, name='dispatch')
class GetTokenView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        token = request.auth
        return Response({"token": token.key}, status=status.HTTP_200_OK)

@method_decorator(csrf_exempt, name='dispatch')
class GetUserView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

@method_decorator(csrf_exempt, name='dispatch')
class AddSequenceDataView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        timestamp = request.data.get('datetime')
        class_idx = int(request.data.get('class_idx'))
        class_name = request.data.get('class_name')
        percent = int(request.data.get('percent'))
        volume = int(request.data.get('volume'))

        if timestamp and class_idx is not None and percent is not None:
            try:
                request.user.add_sequence_data(timestamp, class_idx, class_name, percent, volume)
                return Response({"message": "Sequence data added successfully"}, status=status.HTTP_201_CREATED)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "datetime, class_idx, class_name, percent, volume are required"}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        sequence_data = request.user.get_sequence_data()
        return Response(sequence_data, status=status.HTTP_200_OK)

@method_decorator(csrf_exempt, name='dispatch')    
class AddConversationDataView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        timestamp = request.data.get('datetime')
        text = request.data.get('text')
        emotion_score = int(request.data.get('emotion_score'))

        if timestamp and text is not None and emotion_score is not None:
            try:
                request.user.add_conversation_data(timestamp, text, emotion_score)
                return Response({"message": "Conversation data added successfully"}, status=status.HTTP_201_CREATED)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "datetime, text, emotion_score are required"}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        sequence_data = request.user.get_sequence_data()
        return Response(sequence_data, status=status.HTTP_200_OK)