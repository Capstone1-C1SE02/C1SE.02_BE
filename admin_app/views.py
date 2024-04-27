from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from django.http import JsonResponse
from datetime import datetime
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.pagination import PageNumberPagination

from .models  import *
from .serializers import *

########### Define My Pagination ########
class MyPagination(PageNumberPagination):
    page_size = 10  # Số lượng đối tượng trên mỗi trang

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'total_pages': self.get_total_pages(),  # Tổng số trang
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })

    def get_total_pages(self):
        total_pages = (self.page.paginator.count + self.page_size - 1) // self.page_size
        return total_pages



class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # Xác thực thông tin đăng nhập
        user = authenticate(username=username, password=password)

        if user is not None:
            # Tạo token nếu xác thực thành công
            refresh = RefreshToken.for_user(user)
            message = "Succesfully"
            tokens = {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
            return Response({"token:":tokens ,"message":message}, status=status.HTTP_200_OK)
        else:
            # Trả về lỗi nếu xác thực thất bại
            return Response({"error": "Incorrect username or password."}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            request.user.auth_token.delete()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        


####################################
############ Status Type API ###############

########### Academic Level Type API ########
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class AcademicLevelTypeList(APIView):
    def get(self, request, format=None):
        academicLevelType = academic_level_type.objects.all()
        serializer = AcademicLevelTypeSerializer(academicLevelType, many=True)
        return Response(serializer.data)
    def post(self, request, format=None):
        serializer = AcademicLevelTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data, "message": "Tạo mới thành công"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class AcademicLevelTypeDetail(APIView):
    def get_object(self, pk):
        try:
            return academic_level_type.objects.get(pk=pk)
        except academic_level_type.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        academicLevelType = self.get_object(pk)
        serializer = AcademicLevelTypeSerializer(academicLevelType)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        academicLevelType = self.get_object(pk)
        serializer = AcademicIntakeSessionSerializer(academicLevelType, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        academicLevelType = self.get_object(pk)
        academicLevelType.delete()
        return Response({"message": "Xóa thành công"}, status=status.HTTP_204_NO_CONTENT)

########### Learning  Status Type API ########
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class LearningStatusTypeList(APIView):
    def get(self, request, format=None):
        learningStatusType = learning_status_type.objects.all()
        serializer = LearningStatusTypeSerializer(learningStatusType, many=True)
        return Response(serializer.data)
    def post(self, request, format=None):
        serializer = LearningStatusTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data, "message": "Tạo mới thành công"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class LearningStatusTypeDetail(APIView):
    def get_object(self, pk):
        try:
            return learning_status_type.objects.get(pk=pk)
        except learning_status_type.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        learningStatusType = self.get_object(pk)
        serializer = LearningStatusTypeSerializer(learningStatusType)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        learningStatusType = self.get_object(pk)
        serializer = LearningStatusTypeSerializer(learningStatusType, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        learningStatusType = self.get_object(pk)
        learningStatusType.delete()
        return Response({"message": "Xóa thành công"}, status=status.HTTP_204_NO_CONTENT)












##########################################
################## API ###################
##########################################
####### Academic Intake Session API ########
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class AcademicIntakeSessionList(APIView):
    pagination_class = MyPagination
    def get(self, request, format=None):
        academicIntakeSession = academic_intake_session.objects.all()
        paginator = self.pagination_class()  # Khởi tạo paginator
        result_page = paginator.paginate_queryset(academicIntakeSession, request)
        serializer = AcademicIntakeSessionSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    def post(self, request, format=None):
        serializer = AcademicIntakeSessionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data, "message": "Tạo mới thành công"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class AcademicIntakeSessionDetail(APIView):
    def get_object(self, pk):
        try:
            return academic_intake_session.objects.get(pk=pk)
        except academic_intake_session.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        academicIntakeSession = self.get_object(pk)
        serializer = AcademicIntakeSessionSerializer(academicIntakeSession)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        academicIntakeSession = self.get_object(pk)
        serializer = AcademicIntakeSessionSerializer(academicIntakeSession, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        academicIntakeSession = self.get_object(pk)
        academicIntakeSession.delete()
        return Response({"message": "Xóa thành công"}, status=status.HTTP_204_NO_CONTENT)
    


####### Curriculum API ########
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class CurriculumList(APIView):
    pagination_class = MyPagination
    def get(self, request, format=None):
        curriculum_temp = curriculum.objects.all()
        paginator = self.pagination_class()  # Khởi tạo paginator
        curriculum_page = paginator.paginate_queryset(curriculum_temp, request)
        serializer = GetCurriculumSerializer(curriculum_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    def post(self, request, format=None):
        serializer = PostCurriculumSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data, "message": "Tạo mới thành công"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class CurriculumDetail(APIView):
    def get_object(self, pk):
        try:
            return curriculum.objects.get(pk=pk)
        except curriculum.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        curriculum_temp = self.get_object(pk)
        serializer = GetCurriculumSerializer(curriculum_temp)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        curriculum_temp = self.get_object(pk)
        serializer = PostCurriculumSerializer(curriculum_temp, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        curriculum_temp = self.get_object(pk)
        curriculum_temp.delete()
        return Response({"message": "Xóa thành công"}, status=status.HTTP_204_NO_CONTENT)
    


####### Student API ########
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class StudentList(APIView):
    pagination_class = MyPagination
    def get(self, request, format=None):
        student_list = student.objects.all()
        paginator = self.pagination_class()  # Khởi tạo paginator
        curriculum_page = paginator.paginate_queryset(student_list, request)
        serializer = GetStudentSerializer(curriculum_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    def post(self, request, format=None):
        serializer = PostStudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data, "message": "Tạo mới thành công"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class StudentDetail(APIView):
    def get_object(self, pk):
        try:
            return student.objects.get(pk=pk)
        except student.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        student_temp = self.get_object(pk)
        serializer = GetStudentSerializer(student_temp)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        student_temp = self.get_object(pk)
        serializer = PostStudentSerializer(student_temp, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        student_temp = self.get_object(pk)
        student_temp.delete()
        return Response({"message": "Xóa thành công"}, status=status.HTTP_204_NO_CONTENT)
    


####### Degree API ########
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class DegreeList(APIView):
    pagination_class = MyPagination
    def get(self, request, format=None):
        degree_list = degree.objects.all()
        paginator = self.pagination_class()  # Khởi tạo paginator
        curriculum_page = paginator.paginate_queryset(degree_list, request)
        serializer = DegreeSerializer(curriculum_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    def post(self, request, format=None):
        serializer = DegreeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data, "message": "Tạo mới thành công"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class DegreeDetail(APIView):
    def get_object(self, pk):
        try:
            return degree.objects.get(pk=pk)
        except degree.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        degree_temp = self.get_object(pk)
        serializer = DegreeSerializer(degree_temp)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        degree_temp = self.get_object(pk)
        serializer = DegreeSerializer(degree_temp, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        degree_temp = self.get_object(pk)
        degree_temp.delete()
        return Response({"message": "Xóa thành công"}, status=status.HTTP_204_NO_CONTENT)
    


###### Academic Program API ######
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class AcademicProgramList(APIView):
    pagination_class = MyPagination
    def get(self, request, format=None):
        academic_program_list = academic_program.objects.all()
        paginator = self.pagination_class()
        curriculum_page = paginator.paginate_queryset(academic_program_list, request)
        serializer = GetAcademicProgramSerializer(curriculum_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    def post(self, request, format=None):
        serializer = PostAcademicProgramSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data, "message": "Tạo mới thành công"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class AcademicProgramDetail(APIView):
    def get_object(self, pk):
        try:
            return academic_program.objects.get(pk=pk)
        except academic_program.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        academic_program_temp = self.get_object(pk)
        serializer = GetAcademicProgramSerializer(academic_program_temp)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        academic_program_temp = self.get_object(pk)
        serializer = PostAcademicProgramSerializer(academic_program_temp, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        academic_program_temp = self.get_object(pk)
        academic_program_temp.delete()
        return Response({"message": "Xóa thành công"}, status=status.HTTP_204_NO_CONTENT)