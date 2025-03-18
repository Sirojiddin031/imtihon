from rest_framework import viewsets, status, generics
from rest_framework.generics import ListAPIView
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView, TokenBlacklistView
from .models import *
from .models import Status
from .serializers import *
from django.core.management.base import BaseCommand
from django.db.models import Q
from .serializers import UserAndStudentSerializer
from .serializers import TeacherSerializer
from .permissions import AdminUser
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from faker import Faker
import random
from django.core.management import call_command

fake = Faker()

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserAllSerializer 

    def get_permissions(self):
        if self.action in ['create', 'login']:
            return [AllowAny()]
        return [IsAuthenticated()]

    @action(detail=False, methods=['POST'], permission_classes=[AllowAny])
    def login(self, request):
        phone = request.data.get('phone')
        password = request.data.get('password')
        user = authenticate(phone=phone, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            })
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['POST'], permission_classes=[IsAuthenticated])
    def change_password(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({'message': 'Parol muvaffaqiyatli o‘zgartirildi'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def me(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
        
    @api_view(['GET'])
    def user_list(request):
        users = User.objects.all()
        serializer = UserAllSerializer(users, many=True)
        return Response(serializer.data)
    
class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [AdminUser]

    @swagger_auto_schema(request_body=UserCreateSerializer)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class StudentStatisticView(generics.GenericAPIView):
    serializer_class = StudentStatisticSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=StudentStatisticSerializer)
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            start_date = serializer.validated_data["start_date"]
            end_date = serializer.validated_data["end_date"]
            student_count = Student.objects.filter(created__range=[start_date, end_date]).count()
            return Response({"student_count": student_count}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class TeacherGroupListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, teacher_id):
        groups = Group.objects.filter(teacher__id=teacher_id)
        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class TeacherStatisticView(generics.GenericAPIView):
    serializer_class = TeacherStatisticSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=TeacherStatisticSerializer)
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            start_date = serializer.validated_data["start_date"]
            end_date = serializer.validated_data["end_date"]
            teacher_count = Teacher.objects.filter(created__range=[start_date, end_date]).count()
            return Response({"teacher_count": teacher_count}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AttendanceStatisticView(generics.GenericAPIView):
    serializer_class = AttendanceStatisticSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=AttendanceStatisticSerializer)
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            start_date = serializer.validated_data["start_date"]
            end_date = serializer.validated_data["end_date"]
            attendance_count = Attendance.objects.filter(created__range=[start_date, end_date]).count()
            return Response({"attendance_count": attendance_count}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CourseStatisticView(generics.GenericAPIView):
    serializer_class = CourseStatisticSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=CourseStatisticSerializer)
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            start_date = serializer.validated_data["start_date"]
            end_date = serializer.validated_data["end_date"]
            course_count = Course.objects.filter(created__range=[start_date, end_date]).count()
            return Response({"course_count": course_count}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GroupStatisticView(generics.GenericAPIView):
    serializer_class = GroupStatisticSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=GroupStatisticSerializer)
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            start_date = serializer.validated_data["start_date"]
            end_date = serializer.validated_data["end_date"]
            group_count = Group.objects.filter(created__range=[start_date, end_date]).count()
            return Response({"group_count": group_count}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CreateSuperUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SuperUserCreateSerializer
    permission_classes = [IsAdminUser]  # Faqat admin foydalanuvchilar yaratishi mumkin

    @swagger_auto_schema(request_body=SuperUserCreateSerializer)
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save(is_superuser=True, is_staff=True)
            return Response({"message": "Superuser muvaffaqiyatli yaratildi!", "user_id": user.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class TeacherViewSet(viewsets.ModelViewSet):
    """
    O‘qituvchilar uchun CRUD ViewSet
    """
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [AdminUser]  

    @swagger_auto_schema(request_body=UserAndTeacherSerializer)
    @action(detail=False, methods=['post'], permission_classes=[AdminUser])
    def create_teacher(self, request):
        """
        O‘qituvchi yaratish (User va Teacher ma’lumotlarini birgalikda qabul qiladi)
        """
        user_data = request.data.get('user', {})
        user_serializer = UserSerializer(data=user_data)

        if user_serializer.is_valid():
            user = user_serializer.save(is_teacher=True)
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        teacher_data = request.data.get('teacher', {})
        teacher_serializer = TeacherSerializer(data=teacher_data)

        if teacher_serializer.is_valid():
            teacher_serializer.save(user=user)
            return Response(teacher_serializer.data, status=status.HTTP_201_CREATED)
        else:
            user.delete()
            return Response(teacher_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def teacher_group_list(request, teacher_id):
    teacher = Teacher.objects.get(id=teacher_id)
    groups = teacher.group_set.all()
    serializer = GroupSerializer(groups, many=True)
    return Response(serializer.data)
    
class TeacherListView(ListAPIView):
    queryset = Teacher.objects.all()
    pagination_class = PageNumberPagination
    permission_classes = [AdminUser]
class TeacherListCreateAPIView(generics.ListCreateAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [IsAuthenticated]

class TeacherRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [IsAuthenticated]

# --- Authentication Views ---
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        phone = serializer.validated_data.get('phone')
        password = serializer.validated_data.get('password')
        user = authenticate(request, phone=phone, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            })
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    try:
        refresh_token = request.data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({"message": "Logged out successfully."}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me_view(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

# Attendance
class AttendanceLevelViewSet(viewsets.ModelViewSet):
    queryset = AttendanceLevel.objects.all()
    serializer_class = AttendanceLevelSerializer

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

# Courses 
class CourseViewSet(viewsets.ViewSet):
    permission_classes = [AdminUser]

    def list(self, request):
        courses = Course.objects.all()
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(courses, request)
        serializer = CourseSerializer(result_page, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        course = get_object_or_404(Course, pk=pk)
        serializer = SubjectSerializer(course)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='create/course')
    @swagger_auto_schema(request_body=CourseSerializer)
    def create_course(self, request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put'], url_path='update/course')
    @swagger_auto_schema(request_body=CourseSerializer)
    def update_course(self, request, pk=None):
        course = get_object_or_404(Subject, pk=pk)
        serializer = CourseSerializer(course, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'], url_path='delete/course')
    def delete_course(self, request, pk=None):
        course = get_object_or_404(Course, pk=pk)
        course.delete()
        return Response({'status':True,'detail': 'Cource muaffaqiyatli uchirildi'}, status=status.HTTP_204_NO_CONTENT)


# Groups 
class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    @action(detail=True, methods=['POST'], permission_classes=[IsAuthenticated])
    def students_add(self, request, pk=None):
        group = self.get_object()
        student_id = request.data.get('student_id')
        try:
            student = Student.objects.get(id=student_id)
            group.students.add(student)
            return Response({'detail': 'Student added successfully.'})
        except Student.DoesNotExist:
            return Response({'error': 'Student not found.'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['POST'], permission_classes=[IsAuthenticated])
    def teachers_add(self, request, pk=None):
        group = self.get_object()
        teacher_id = request.data.get('teacher_id')
        try:
            teacher = Worker.objects.get(id=teacher_id)
            group.teachers.add(teacher)
            return Response({'detail': 'Teacher added successfully.'})
        except Worker.DoesNotExist:
            return Response({'error': 'Teacher not found.'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['POST'], permission_classes=[IsAuthenticated])
    def students_remove(self, request, pk=None):
        group = self.get_object()
        student_id = request.data.get('student_id')
        try:
            student = Student.objects.get(id=student_id)
            group.students.remove(student)
            return Response({'detail': 'Student removed successfully.'})
        except Student.DoesNotExist:
            return Response({'error': 'Student not found.'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['POST'], permission_classes=[IsAuthenticated])
    def teachers_remove(self, request, pk=None):
        group = self.get_object()
        teacher_id = request.data.get('teacher_id')
        try:
            teacher = Worker.objects.get(id=teacher_id)
            group.teachers.remove(teacher)
            return Response({'detail': 'Teacher removed successfully.'})
        except Worker.DoesNotExist:
            return Response({'error': 'Teacher not found.'}, status=status.HTTP_404_NOT_FOUND)

# Homework
class GroupHomeWorkViewSet(viewsets.ModelViewSet):
    queryset = GroupHomeWork.objects.all()
    serializer_class = GroupHomeWorkSerializer

class HomeWorkViewSet(viewsets.ModelViewSet):
    queryset = HomeWork.objects.all()
    serializer_class = HomeWorkSerializer

# Table Types 
class TableTypeViewSet(viewsets.ModelViewSet):
    queryset = TableType.objects.all()
    serializer_class = TableTypeSerializer

class TableViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer

# Student va Parent

class StudentViewSet(viewsets.ModelViewSet):
    """Student CRUD API - qo'shish, ko'rish, yangilash, o‘chirish"""
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]


    def create(self, request, *args, **kwargs):
        """Yangi student qo‘shish"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": True, "message": "Student muvaffaqiyatli qo‘shildi!", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"status": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['GET'])
    def studying(self, request):
        """O‘qiyotgan studentlar"""
        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")
        if not start_date or not end_date:
            return Response({"error": "start_date va end_date berilishi shart!"}, status=400)

        students = Student.objects.filter(
            Q(group__start_date__lte=end_date) & Q(group__end_date__gte=start_date)
        ).distinct()

        serializer = self.get_serializer(students, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def graduated(self, request):
        """Bitirgan studentlar"""
        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")
        if not start_date or not end_date:
            return Response({"error": "start_date va end_date berilishi shart!"}, status=400)

        students = Student.objects.filter(
            Q(group__end_date__gte=start_date) & Q(group__end_date__lte=end_date)
        ).distinct()

        serializer = self.get_serializer(students, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def enrolled(self, request):
        """Qabul qilingan studentlar"""
        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")
        if not start_date or not end_date:
            return Response({"error": "start_date va end_date berilishi shart!"}, status=400)

        students = Student.objects.filter(
            Q(created__gte=start_date) & Q(created__lte=end_date)
        ).distinct()

        serializer = self.get_serializer(students, many=True)
        return Response(serializer.data)

class ParentsViewSet(viewsets.ModelViewSet):
    queryset = Parents.objects.all()
    serializer_class = ParentSerializer

# Worker 
class WorkerViewSet(viewsets.ModelViewSet):
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer

# Comment 
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [AdminUser]
        
class Command(BaseCommand):
    help = "Generate mock data for testing"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Generating mock data..."))

        for _ in range(10):
            user = User.objects.create(
                phone=fake.phone_number(),
                full_name=fake.name(),
                is_student=True
            )
            Student.objects.create(user=user, descriptions=fake.text())

        for _ in range(5):
            user = User.objects.create(
                phone=fake.phone_number(),
                full_name=fake.name(),
                is_teacher=True
            )
            Teacher.objects.create(user=user, descriptions=fake.text())

        self.stdout.write(self.style.SUCCESS("Mock data successfully created!"))

class PopulateMockDataView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        try:
            call_command('populate_mock_data')  # Django management buyruqni chaqirish
            return Response({"message": "Mock data successfully created!"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Password 
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=ChangePasswordSerializer)
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            request.user.set_password(serializer.validated_data['new_password'])
            request.user.save()
            return Response({"message": "Parol muvaffaqiyatli o‘zgartirildi"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
    """
    Foydalanuvchi login API'si
    """
    @staticmethod
    def get_tokens_for_user(user):
        """
        Foydalanuvchi uchun JWT tokenlarni yaratish
        """
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request):
        phone = request.data.get("phone")
        password = request.data.get("password")

        user = User.objects.filter(phone=phone).first()

        if user and user.check_password(password):
            tokens = self.get_tokens_for_user(user)
            return Response(tokens, status=status.HTTP_200_OK)

        return Response(
            {"status": False, "detail": "Telefon raqam yoki parol noto‘g‘ri"},
            status=status.HTTP_401_UNAUTHORIZED
        )

class LogoutView(APIView):
    """
    Foydalanuvchini tizimdan chiqarish (logout)
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()  # 🔹 Tokenni qora ro‘yxatga qo‘shish

            return Response({"message": "Logout muvaffaqiyatli bajarildi"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

#  Parolni tiklash
class ResetPasswordAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            return Response({"message": "OTP muvaffaqiyatli yuborildi"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# OTP ni tk
class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=VerifyOTPSerializer)
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data["phone"]
            otp = serializer.validated_data["otp"]
            user = User.objects.filter(phone=phone, otp_code=otp).first()

            if user:
                return Response({"message": "OTP to‘g‘ri"}, status=status.HTTP_200_OK)

            return Response({"status": False, "detail": "OTP tasdiqlanmagan"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MockDataViewSet(viewsets.ModelViewSet):
    queryset = MockData.objects.all()
    serializer_class = MockDataSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['POST'])
    def populate(self, request):
        # Mock ma'lumotlar
        data_samples = [
            {"name": "Test 1", "description": "Birinchi test ma'lumoti"},
            {"name": "Test 2", "description": "Ikkinchi test ma'lumoti"},
            {"name": "Test 3", "description": "Uchinchi test ma'lumoti"},
        ]
        for data in data_samples:
            MockData.objects.create(**data)

        return Response({"message": "Mock data successfully populated!"}, status=201)

# Yangi parol
class SetNewPasswordAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SetNewPasswordSerializer(data=request.data)
        if serializer.is_valid():
            return Response({"message": "Parol muvaffaqiyatli o‘zgartirildi"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Tokenni yangilash
class CustomTokenRefreshView(TokenRefreshView):
    """Refresh token orqali yangi access token yaratish"""
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            return Response({
                "status": True,
                "message": "Token muvaffaqiyatli yangilandi",
                "data": response.data
            })
        return Response({
            "status": False,
            "detail": "Token yaroqsiz yoki muddati tugagan",
            "code": "token_not_valid"
        }, status=status.HTTP_401_UNAUTHORIZED)    
    
class CustomTokenRefreshView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = TokenRefreshSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProtectedAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "Siz muvaffaqiyatli autentifikatsiyadan o‘tdingiz!"})


class TeacherCreateAPIView(APIView):
    permission_classes = [AdminUser]

    @swagger_auto_schema(request_body=UserAndTeacherSerializer)
    def post(self, request):
        user_data = request.data.get('user', {})
        user_serializer = UserSerializer(data=user_data)

        if user_serializer.is_valid():
            user = user_serializer.save(is_teacher=True)
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        teacher_data = request.data.get('teacher', {})   
        teacher_serializer = TeacherSerializer(data=teacher_data)

        if teacher_serializer.is_valid():
            teacher_serializer.save(user=user)
            return Response(teacher_serializer.data, status=status.HTTP_201_CREATED)

        else:
            user.delete()
            return Response(teacher_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StudentCreateAPIView(APIView):
    permission_classes = [AdminUser]

    @swagger_auto_schema(request_body=UserAndStudentSerializer)
    def post(self, request):

        user_data = request.data.get('user', {})
        user_serializer = UserSerializer(data=user_data)

        if user_serializer.is_valid():
            user = user_serializer.save(is_student=True)
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        student_data = request.data.get('student', {})
        student_serializer = StudentSerializer(data=student_data)

        if student_serializer.is_valid():
            student = student_serializer.save(user=user)
            return Response(student_serializer.data, status=status.HTTP_201_CREATED)

        else:
            user.delete()
            return Response(student_serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class StudentGroupsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, student_id):
        """ Talabaning barcha guruhlarini olish """
        student = get_object_or_404(Student, id=student_id)
        groups = student.group.all()  
        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data)

    def post(self, request, student_id):
        """ Talabani yangi guruhga qo‘shish """
        student = get_object_or_404(Student, id=student_id)
        group_id = request.data.get("group_id")

        if not group_id:
            return Response({"error": "group_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        group = get_object_or_404(Group, id=group_id)
        student.group = group  # Asosiy guruh sifatida
        student.save()
        student.group.add(group)  # Qo‘shimcha guruh sifatida ham qo‘shiladi
        
        return Response({"message": f"Student added to {group.name}"}, status=status.HTTP_201_CREATED)

    def delete(self, request, student_id):
        """ Talabani guruhdan o‘chirish """
        student = get_object_or_404(Student, id=student_id)
        group_id = request.data.get("group_id")

        if not group_id:
            return Response({"error": "group_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        group = get_object_or_404(Group, id=group_id)

        if group in student.group.all():
            student.group.remove(group)
            return Response({"message": f"Student removed from {group.name}"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Student is not in this group"}, status=status.HTTP_400_BAD_REQUEST)

class StudentAttendanceListView(generics.ListAPIView):
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        student_id = self.kwargs['student_id']
        return Attendance.objects.filter(student__id=student_id)


class StudentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]

class StudentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]
    
class CurrentUserView(RetrieveAPIView):
    serializer_class = MeSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    
class DecoratedTokenObtainPairView(TokenObtainPairView):
    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: TokenObtainPairResponseSerializer,
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class DecoratedTokenRefreshView(TokenRefreshView):
    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: TokenRefreshResponseSerializer,
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class DecoratedTokenVerifyView(TokenVerifyView):
    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: TokenVerifyResponseSerializer,
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class DecoratedTokenBlacklistView(TokenBlacklistView):
    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: TokenBlacklistResponseSerializer,
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class StatusViewSet(viewsets.ViewSet): #Status 

    permission_classes = [AdminUser]

    def list(self, request):

        statuses = Status.objects.all()
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(statuses, request)
        serializer = StatusSerializer(result_page, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):

        status_obj = get_object_or_404(Status, pk=pk)
        serializer = StatusSerializer(status_obj)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='create')
    @swagger_auto_schema(request_body=StatusSerializer)
    def create_status(self, request): 

        serializer = StatusSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put'], url_path='update')
    @swagger_auto_schema(request_body=StatusSerializer)
    def update_status(self, request, pk=None):

        status_obj = get_object_or_404(Status, pk=pk)
        serializer = StatusSerializer(status_obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'], url_path='delete')
    def delete_status(self, request, pk=None): 

        status_obj = get_object_or_404(Status, pk=pk)
        status_obj.delete()
        return Response({'status': True, 'detail': 'Status muvaffaqiyatli o‘chirildi'}, status=status.HTTP_204_NO_CONTENT)
