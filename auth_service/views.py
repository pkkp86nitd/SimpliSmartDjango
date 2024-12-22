from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Organization
from .serializers import UserSerializer, OrganizationSerializer

class RegisterUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Register a new user and return JWT tokens (access and refresh).
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return Response({
                'access': access_token,
                'refresh': str(refresh)
            }, status=201)
        return Response(serializer.errors, status=400)


class LoginUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Login the user and return JWT tokens (access and refresh).
        """
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({"error": "Username and password are required."}, status=400)

        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                # Generate JWT tokens
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)

                return Response({
                    'access': access_token,
                    'refresh': str(refresh)
                }, status=200)
            else:
                return Response({"error": "Invalid credentials."}, status=400)
        except User.DoesNotExist:
            return Response({"error": "Invalid credentials."}, status=400)


class OrganizationInviteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Allow the logged-in user to join an organization using the invite code.
        """
        invite_code = request.data.get('invite_code')

        if not invite_code:
            return Response({"error": "Invite code is required."}, status=400)

        try:
            organization = Organization.objects.get(invite_code=invite_code)
            user = request.user  # Get the currently logged-in user
            user.organization = organization
            user.save()

            return Response({"message": "Successfully joined the organization."}, status=200)
        except Organization.DoesNotExist:
            return Response({"error": "Invalid invite code."}, status=400)

