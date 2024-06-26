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
from django.shortcuts import render
from .forms import ExcelUploadForm
import pandas as pd
from django.db import IntegrityError
from django.db import transaction
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import api_view
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
####### Academic Intake Session API #######
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class AcademicIntakeSessionList(APIView):
    pagination_class = MyPagination
    def get(self, request, format=None):
        academicIntakeSession = academic_intake_session.objects.all()
        if 'page' in request.query_params:
            paginator = self.pagination_class()  # Khởi tạo paginator
            result_page = paginator.paginate_queryset(academicIntakeSession, request)
            serializer = AcademicIntakeSessionSerializer(result_page, many=True)
            return paginator.get_paginated_response({"data":serializer.data, "errCode":"0"})
        else:
            # If 'page' is not in request, return all results
            serializer = AcademicIntakeSessionSerializer(academicIntakeSession, many=True)
            return Response({"data":serializer.data, "errCode":"0"})
    def post(self, request, format=None):
        serializer = AcademicIntakeSessionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data, "message": "Tạo mới thành công","errCode":"0"}, status=status.HTTP_201_CREATED)
        return Response({"Error":serializer.errors, "errCode":"-1"}, status=status.HTTP_400_BAD_REQUEST)

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
        return Response({"data":serializer.data, "errCode":"0"},status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        academicIntakeSession = self.get_object(pk)
        serializer = AcademicIntakeSessionSerializer(academicIntakeSession, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data,"errCode":"0", "message": "Chỉnh sửa thành công"},status=status.HTTP_200_OK)
        return Response({"Error":serializer.errors, "errCode":"-1"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        academicIntakeSession = self.get_object(pk)
        academicIntakeSession.delete()
        return Response({"message": "Xóa thành công","errCode":"0"}, status=status.HTTP_204_NO_CONTENT)
    


####### Curriculum API ########
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class CurriculumList(APIView):
    pagination_class = MyPagination
    def get(self, request, format=None):
        curriculum_temp = curriculum.objects.all()
        if 'page' in request.query_params:
            paginator = self.pagination_class()  # Khởi tạo paginator
            curriculum_page = paginator.paginate_queryset(curriculum_temp, request)
            serializer = GetCurriculumSerializer(curriculum_page, many=True)
            return paginator.get_paginated_response({"data":serializer.data, "errCode":"0"})
        else:
            # If 'page' is not in request, return all results
            serializer = GetCurriculumSerializer(curriculum_temp, many=True)
            return Response({"data":serializer.data, "errCode":"0"})
    def post(self, request, format=None):
        serializer = PostCurriculumSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data, "message": "Tạo mới thành công","errCode":"0"}, status=status.HTTP_201_CREATED)
        return Response({"Error":serializer.errors, "errCode":"-1"}, status=status.HTTP_400_BAD_REQUEST)

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
        return Response({"data":serializer.data, "errCode":"0"},status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        curriculum_temp = self.get_object(pk)
        serializer = PostCurriculumSerializer(curriculum_temp, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data,"errCode":"0", "message": "Chỉnh sửa thành công"},status=status.HTTP_200_OK)
        return Response({"Error":serializer.errors, "errCode":"-1"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        curriculum_temp = self.get_object(pk)
        curriculum_temp.delete()
        return Response({"message": "Xóa thành công","errCode":"0"}, status=status.HTTP_204_NO_CONTENT)
    
## Search Curriculum API ##
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class SearchCurriculum(APIView):
    def post(self, request, format=None):
        # Get the 'academicprogramname' query parameter from the request
        academic_program_name = request.query_params.get('academicprogramname', None)
        if academic_program_name is None:
            return Response(
                {"Message": "Vui lòng cung cấp tên chương trình đào tạo để tìm kiếm", "errCode": "-1"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            academic_program_ob = academic_program.objects.get(ACADEMIC_PROGRAM_NAME=academic_program_name)
            academic_program_id = academic_program_ob.ACADEMIC_PROGRAM_ID
            curriculum_information = curriculum.objects.filter(ACADEMIC_PROGRAM_ID=academic_program_id)
            if curriculum_information.exists():
                serializer = GetCurriculumSerializer(curriculum_information, many=True)
                return Response(
                    {"data": serializer.data, "Message": "Lấy dữ liệu thành công!!", "errCode": "0"}, 
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"Message": "Không tìm thấy chương trình đào tạo phù hợp!!", "errCode": "-1"}, 
                    status=status.HTTP_404_NOT_FOUND
                )
        except academic_program.DoesNotExist:
            return Response(
                {"Message": "Không tìm thấy chương trình đào tạo phù hợp!!", "errCode": "-1"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"Message": "Đã xảy ra lỗi khi tìm kiếm chương trình đào tạo", "errCode": "-1", "error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )



####### Student API ########
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class StudentList(APIView):
    pagination_class = MyPagination
    def get(self, request, format=None):
        student_list = student.objects.all()
        if 'page' in request.query_params:
            paginator = self.pagination_class()
            result_page = paginator.paginate_queryset(student_list, request)
            serializer = GetStudentSerializer(result_page, many=True)
            return paginator.get_paginated_response({"data": serializer.data, "Message": "Trả kết quả theo page!!", "errCode": "0"})
        else:
            # If 'page' is not in request, return all results
            serializer = GetStudentSerializer(student_list, many=True)
            return Response({"data": serializer.data, "Message": "Trả All!!", "errCode": "0"})
    def post(self, request, format=None):
        serializer = PostStudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data, "message": "Tạo mới thành công","errCode":"0"}, status=status.HTTP_201_CREATED)
        return Response({"Error":serializer.errors, "errCode":"-1"}, status=status.HTTP_400_BAD_REQUEST)

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
        return Response({"data":serializer.data, "errCode":"0"},status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        student_temp = self.get_object(pk)
        serializer = PostStudentSerializer(student_temp, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data,"errCode":"0", "message": "Chỉnh sửa thành công"},status=status.HTTP_200_OK)
        return Response({"Error":serializer.errors, "errCode":"-1"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        student_temp = self.get_object(pk)
        student_temp.delete()
        return Response({"message": "Xóa thành công","errCode":"0"}, status=status.HTTP_204_NO_CONTENT)
    
## Search Student API ##
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class SearchStudent(APIView):
    def post(self, request, format=None):
        # Get the 'name' query parameter from the request
        student_id= request.query_params.get('studentID', None)

        if student_id:
            try:
                student_information = student.objects.filter(STUDENT_ID_NUMBER__startswith=student_id)
                if student_information.exists():
                    serializer = GetStudentSerializer(student_information, many=True)
                    return Response({"data": serializer.data, "Message": "Lấy dữ liệu thành công!!", "errCode": "0"}, status=status.HTTP_200_OK)
                else:
                    return Response({"Message": "Không tìm thấy sinh viên phù hợp!!", "errCode": "-1"}, status=status.HTTP_404_NOT_FOUND)
            except:
                return Response({"Message": "Không tìm thấy sinh viên phù hợp!!", "errCode": "-1"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"Message": "Vui lòng cung cấp mã sinh viên để tìm kiếm", "errCode": "-1"}, status=status.HTTP_400_BAD_REQUEST)     
######----------------------------------------------------------------------------------------------#####


####### Degree API ########
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class DegreeList(APIView):
    pagination_class = MyPagination
    def get(self, request, format=None):
        degree_list = degree.objects.all()
        # Check if 'page' parameter is present in the request
        if 'page' in request.query_params:
            paginator = self.pagination_class()
            result_page = paginator.paginate_queryset(degree_list, request)
            serializer = DegreeSerializer(result_page, many=True)
            return paginator.get_paginated_response({"data": serializer.data,"message":"Trả kết quả theo page" ,"errCode": "0"})
        else:
            # If 'page' is not in request, return all results
            serializer = DegreeSerializer(degree_list, many=True)
            return Response({"data": serializer.data,"message":"Trả All" , "errCode": "0"})
    def post(self, request, format=None):
        
        if degree.objects.filter(DEGREE_NAME=request.data['DEGREE_NAME']).exists():
            return Response({"Error":"Tên ngành đã tồn tại!! Vui lòng xem lại", "errCode":"-1"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = DegreeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()   
            return Response({"data": serializer.data, "message": "Tạo mới thành công","errCode":"0"}, status=status.HTTP_201_CREATED)
        return Response({"Error":serializer.errors, "errCode":"-1"}, status=status.HTTP_400_BAD_REQUEST)

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
        return Response({"data":serializer.data, "errCode":"0"},status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        degree_temp = self.get_object(pk)
        serializer = DegreeSerializer(degree_temp, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data,"errCode":"0", "message": "Chỉnh sửa thành công"},status=status.HTTP_200_OK)
        return Response({"Error":serializer.errors, "errCode":"-1"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        degree_temp = self.get_object(pk)
        degree_temp.delete()
        return Response({"message": "Xóa thành công","errCode":"0"}, status=status.HTTP_204_NO_CONTENT)


### Search Degree API ###
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class SearchDegree(APIView):
    def post(self, request, format=None):
        # Get the 'degree name' query parameter from the request
        degree_name= request.query_params.get('degreename', None)

        if degree_name:
            # Filter students by name (case-insensitive)
            try:
                degree_information = degree.objects.filter(DEGREE_NAME__icontains=degree_name)
                if degree_information.exists():
                    serializer = DegreeSerializer(degree_information, many=True)
                    return Response({"data": serializer.data, "Message": "Lấy dữ liệu thành công!!", "errCode": "0"}, status=status.HTTP_200_OK)
                else:
                    return Response({"Message": "Không tìm thấy tên ngành phù hợp!", "errCode": "-1"}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({"Message": "Đã xảy ra lỗi khi tìm kiếm ngành", "errCode": "-1", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"Message": "Vui lòng cung cấp tên ngành để tìm kiếm", "errCode": "-1"}, status=status.HTTP_400_BAD_REQUEST)



######----------------------------------------------------------------------------------------------#####  


###### Academic Program API ######
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class AcademicProgramList(APIView):
    pagination_class = MyPagination
    def get(self, request, format=None):
        academic_program_list = academic_program.objects.all()
        if 'page' in request.query_params:
            paginator = self.pagination_class()
            academic_program_page = paginator.paginate_queryset(academic_program_list, request)
            serializer = GetAcademicProgramSerializer(academic_program_page, many=True)
            return paginator.get_paginated_response({"data": serializer.data,"message":"Trả kết quả theo page!!", "errCode": "0"})
        else:
            # If 'page' is not in request, return all results
            serializer = GetAcademicProgramSerializer(academic_program_list, many=True)
            return Response({"data": serializer.data,"message":"Trả all !!", "errCode": "0"})
    
    def post(self, request, format=None):
        if academic_program.objects.filter(ACADEMIC_PROGRAM_NAME=request.data['ACADEMIC_PROGRAM_NAME']).exists():
            return Response(
                {"Error": "Tên ngành đã tồn tại!! Vui lòng xem lại", "errCode": "-1"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = PostAcademicProgramSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data, "message": "Tạo mới thành công","errCode":"0"}, status=status.HTTP_201_CREATED)
        return Response({"Error":serializer.errors, "errCode":"-1"}, status=status.HTTP_400_BAD_REQUEST)

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
        return Response({"data":serializer.data, "errCode":"0"},status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        academic_program_temp = self.get_object(pk)
        serializer = PostAcademicProgramSerializer(academic_program_temp, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data,"errCode":"0", "message": "Chỉnh sửa thành công"},status=status.HTTP_200_OK)
        return Response({"Error":serializer.errors, "errCode":"-1"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        academic_program_temp = self.get_object(pk)
        academic_program_temp.delete()
        return Response({"message": "Xóa thành công","errCode":"0"}, status=status.HTTP_204_NO_CONTENT)


### Search Academic Program API ###
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class SearchAcademicProgram(APIView):
    def post(self, request, format=None):
        # Get the 'name' query parameter from the request
        academic_program_name= request.query_params.get('academicprogramname', None)

        if academic_program_name:
            try:
                academic_program_information = academic_program.objects.filter(ACADEMIC_PROGRAM_NAME__startswith=academic_program_name)
                if academic_program_information.exists():
                    serializer = GetAcademicProgramSerializer(academic_program_information, many=True)
                    return Response({"data": serializer.data, "Message": "Lấy dữ liệu thành công!!", "errCode": "0"}, status=status.HTTP_200_OK)
                else:
                    return Response({"Message": "Không tìm thấy chuyên ngành phù hợp!!", "errCode": "-1"}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({"Message": "Đã xảy ra lỗi khi tìm kiếm chuyên ngành", "errCode": "-1", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"Message": "Vui lòng cung cấp tên chuyên ngành để tìm kiếm", "errCode": "-1"}, status=status.HTTP_400_BAD_REQUEST)

######----------------------------------------------------------------------------------------------#####   


###### AcademicIntakeSession AcademicProgram Curriculum API ######
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class AcademicIntakeSession_AcademicProgram_Curriculum_List(APIView):
    pagination_class = MyPagination
    def get(self, request, format=None):
        academicIntakeSession_AcademicProgram_Curriculum_list = academic_intake_session_academic_program_curriculum.objects.all()
        paginator = self.pagination_class()
        academicIntakeSession_AcademicProgram_Curriculum_page = paginator.paginate_queryset(academicIntakeSession_AcademicProgram_Curriculum_list, request)
        serializer = Get_AcademicIntakeSession_AcademicProgram_Curriculum_Serializers(academicIntakeSession_AcademicProgram_Curriculum_page, many=True)
        return paginator.get_paginated_response({"data":serializer.data, "errCode":"0"})
    def post(self, request, format=None):
        serializer = Post_AcademicIntakeSession_AcademicProgram_Curriculum_Serializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data, "message": "Tạo mới thành công","errCode":"0"}, status=status.HTTP_201_CREATED)
        return Response({"Error":serializer.errors, "errCode":"-1"}, status=status.HTTP_400_BAD_REQUEST)

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class AcademicIntakeSession_AcademicProgram_Curriculum_Detail(APIView):
    def get_object(self, pk):
        try:
            return academic_intake_session_academic_program_curriculum.objects.get(pk=pk)
        except academic_intake_session_academic_program_curriculum.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        academicIntakeSession_AcademicProgram_Curriculum_temp = self.get_object(pk)
        serializer = Get_AcademicIntakeSession_AcademicProgram_Curriculum_Serializers(academicIntakeSession_AcademicProgram_Curriculum_temp)
        return Response({"data":serializer.data, "errCode":"0"},status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        academicIntakeSession_AcademicProgram_Curriculum_temp = self.get_object(pk)
        serializer = Post_AcademicIntakeSession_AcademicProgram_Curriculum_Serializers(academicIntakeSession_AcademicProgram_Curriculum_temp, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data,"errCode":"0", "message": "Chỉnh sửa thành công"},status=status.HTTP_200_OK)
        return Response({"Error":serializer.errors, "errCode":"-1"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        academicIntakeSession_AcademicProgram_Curriculum_temp = self.get_object(pk)
        academicIntakeSession_AcademicProgram_Curriculum_temp.delete()
        return Response({"message": "Xóa thành công","errCode":"0"}, status=status.HTTP_204_NO_CONTENT)
    
###### Student AcademicIntakeSession AcademicProgram API ######
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class Student_AcademicIntakeSession_AcademicProgram_List(APIView):
    pagination_class = MyPagination
    def get(self, request, format=None):
        student_AcademicIntakeSession_AcademicProgram_list = student_academic_intake_session_academic_program.objects.all()
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(student_AcademicIntakeSession_AcademicProgram_list, request)
        serializer = Get_Student_AcademicIntakeSession_AcademicProgram_Serializers(result_page, many=True)
        return paginator.get_paginated_response({"data":serializer.data, "errCode":"0"})
    def post(self, request, format=None):
        serializer = Post_Student_AcademicIntakeSession_AcademicProgram_Serializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data, "message": "Tạo mới thành công","errCode":"0"}, status=status.HTTP_201_CREATED)
        return Response({"Error":serializer.errors, "errCode":"-1"}, status=status.HTTP_400_BAD_REQUEST)
    
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class Student_AcademicIntakeSession_AcademicProgram_Detail(APIView):
    def get_object(self, pk):
        try:
            return student_academic_intake_session_academic_program.objects.get(pk=pk)
        except student_academic_intake_session_academic_program.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        student_AcademicIntakeSession_AcademicProgram_temp = self.get_object(pk)
        serializer = Get_Student_AcademicIntakeSession_AcademicProgram_Serializers(student_AcademicIntakeSession_AcademicProgram_temp)
        return Response({"data":serializer.data, "errCode":"0"},status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        student_AcademicIntakeSession_AcademicProgram_temp = self.get_object(pk)
        serializer = Post_Student_AcademicIntakeSession_AcademicProgram_Serializers(student_AcademicIntakeSession_AcademicProgram_temp, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data,"errCode":"0", "message": "Chỉnh sửa thành công"},status=status.HTTP_200_OK)
        return Response({"Error":serializer.errors, "errCode":"-1"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        student_AcademicIntakeSession_AcademicProgram_temp = self.get_object(pk)
        student_AcademicIntakeSession_AcademicProgram_temp.delete()
        return Response({"message": "Xóa thành công"}, status=status.HTTP_204_NO_CONTENT)
    
######### Diploma Management Profile API ###########
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class DiplomaManagementProfileList(APIView):
    pagination_class = MyPagination
    def get(self, request, format=None):
        diplomaManagementProfile = diploma_management_profile.objects.all()
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(diplomaManagementProfile, request)
        serializer = GetDiplomaManagementProfileSerializer(result_page, many=True)
        return paginator.get_paginated_response({"data":serializer.data, "errCode":"0"})
    def post(self, request, format=None):
        serializer = PostDiplomaManagementProfileSerializer(data=request.data)
        if serializer.is_valid():
            if student.objects.filter(STUDENT_ID_NUMBER=request.data['STUDENT_ID_NUMBER']).exists():
                serializer.save()
                return Response({"data": serializer.data, "message": "Tạo mới thành công","errCode":"0"}, status=status.HTTP_201_CREATED)
        return Response({"Error":serializer.errors, "errCode":"-1"}, status=status.HTTP_400_BAD_REQUEST)

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class DiplomaManagementProfileDetail(APIView):
    def get_object(self, pk):
        try:
            return diploma_management_profile.objects.get(pk=pk)
        except diploma_management_profile.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        diplomaManagementProfile = self.get_object(pk)
        serializer = GetDiplomaManagementProfileSerializer(diplomaManagementProfile)
        return Response({"data":serializer.data, "errCode":"0"},status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        diplomaManagementProfile = self.get_object(pk)
        serializer = PostDiplomaManagementProfileSerializer(diplomaManagementProfile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data,"errCode":"0", "message": "Chỉnh sửa thành công"},status=status.HTTP_200_OK)
        return Response({"Error":serializer.errors, "errCode":"-1"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        diplomaManagementProfile = self.get_object(pk)
        diplomaManagementProfile.delete()
        return Response({"message": "Xóa thành công","errCode":"0"}, status=status.HTTP_204_NO_CONTENT)
    

######### import student excel ###########
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class UploadStudentExcel(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Kiểm tra xem tệp có tồn tại trong request hay không
        if 'file' not in request.FILES:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Lấy tệp từ request
        excel_file = request.FILES['file']
        if not excel_file.name.endswith('.xlsx'):
            return Response({"error": "File is not an Excel file"}, status=status.HTTP_400_BAD_REQUEST)
        # Đọc tệp Excel
        try:
            df = pd.read_excel(excel_file)
        except Exception as e:
            return Response({"error": f"Error reading Excel file: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        # Duyệt qua từng hàng của dataframe
        
        errors = []
        valid_data = []
        processed_student_ids = set()

        # Kiểm tra tất cả các dòng
        for index, row in df.iterrows():
            try:
                # Lấy STUDENT_ID_NUMBER từ hàng
                student_id_number = row['Mã Sinh Viên']
                
                # Kiểm tra xem STUDENT_ID_NUMBER có tồn tại trong cơ sở dữ liệu không
                if student.objects.filter(STUDENT_ID_NUMBER=student_id_number).exists():
                    errors.append({"row": index, "error": f"Sinh viên có mã số '{student_id_number}' đã tồn tại trong database!"})
                    continue

                # Kiểm tra xem STUDENT_ID_NUMBER đã được có trong valid_data hay không
                if student_id_number in processed_student_ids:
                    errors.append({"row": index, "error": f"Student ID '{student_id_number}' đã tồn tại trong dữ liệu đầu vào"})
                    continue

                # Chuyển đổi giới tính
                gender = True if row['Giới tính'] == 'Nam' else False

                # Tìm kiếm instance cho các ForeignKey
                learning_status_instance = learning_status_type.objects.filter(LEARNING_STATUS_TYPE_NAME=row['Trạng thái học tập']).first()
                if learning_status_instance is None:
                    errors.append({"row": index, "error": f"Learning status type '{row['Trạng thái học tập']}' không tồn tại"})
                    continue

                academic_level_instance = academic_level_type.objects.filter(ACADEMIC_LEVEL_TYPE_NAME=row['Bậc đào tạo']).first()
                if academic_level_instance is None:
                    errors.append({"row": index, "error": f"Academic level type '{row['Bậc đào tạo']}' không tồn tại"})
                    continue

                processed_student_ids.add(student_id_number)

                # Chuẩn bị dữ liệu hợp lệ
                valid_data.append(student(
                    STUDENT_ID_NUMBER=student_id_number,
                    LAST_NAME=row['Họ'],
                    FIRST_NAME=row['Tên'],
                    MIDDLE_NAME=row['Tên lót'],
                    GENDER=gender,
                    BIRTH_DATE=row['Ngày sinh'],
                    BIRTH_PLACE=row['Nơi sinh'],
                    PEOPLE_ID_NUMBER=row['CCCD'],
                    NATION=row['Dân tộc'],
                    NATIONALITY=row['Quốc tịch'],
                    PHONE_NUMBER=row['Số điện thoại'],
                    EMAIL=row['Email'],
                    COMMENTS=row['Mô tả'],
                    LEARNING_STATUS_TYPE_ID=learning_status_instance,
                    ACADEMIC_LEVEL_TYPE_ID=academic_level_instance,
                ))
                
            except ValidationError as e:
                errors.append({"row": index, "error": dict(e)})
            except Exception as e:
                errors.append({"row": index, "error": str(e)})

        # Nếu có lỗi, trả về các lỗi này
        if errors:
            return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)
        # Nếu không có lỗi, thêm tất cả dữ liệu hợp lệ vào cơ sở dữ liệu
        try:
            with transaction.atomic():
                for student_instance in valid_data:
                    student_instance.save()
        except IntegrityError:
            return Response({"error": "Duplicate student record or integrity error"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"Error saving student: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"success": "Students imported successfully"}, status=status.HTTP_201_CREATED)


######### import diploma excel ###########
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class UploadDiplomaExcel(APIView):
    def post(self, request, format=None):
        # Kiểm tra xem tệp có tồn tại trong request hay không
        if 'file' not in request.FILES:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)
        # Lấy tệp từ request
        excel_file = request.FILES['file']
        if not excel_file.name.endswith('.xlsx'):
            return Response({"error": "File is not an Excel file"}, status=status.HTTP_400_BAD_REQUEST)
        # Đọc tệp Excel
        try:
            df = pd.read_excel(excel_file)
        except Exception as e:
            return Response({"error": f"Error reading Excel file: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        
        
        errors = []
        valid_data = []
        processed_student_ids = set()
        # Kiểm tra tất cả các dòng
        for index, row in df.iterrows():
            try:
                student_instance = student.objects.get(STUDENT_ID_NUMBER=row['Mã sinh viên'])
                academic_program_instance = academic_program.objects.get(ACADEMIC_PROGRAM_NAME=row['Chuyên ngành đào tạo'])

                if diploma_management_profile.objects.filter(STUDENT_ID_NUMBER=row['Mã sinh viên']).exists():
                    errors.append({"row": index, "error": f"Student ID '{row['Mã sinh viên']}' đã tồn tại trong hồ sơ bằng"})
                    continue
                
                if student_instance.STUDENT_ID_NUMBER in processed_student_ids:
                    errors.append({"row": index, "error": f"Student ID '{row['Mã sinh viên']}' đã tồn tại trong dữ liệu đầu vào"})
                    continue
                processed_student_ids.add(student_instance.STUDENT_ID_NUMBER)
                
                # Lấy user từ request (người gửi request)
                user = request.user
                # Chuẩn bị dữ liệu hợp lệ
                valid_data.append(diploma_management_profile(
                    STUDENT_ID_NUMBER=student_instance,
                    ACADEMIC_PROGRAM_ID=academic_program_instance,
                    GRADUATION_YEAR=row['Năm tốt nghiệp'],
                    MODE_OF_STUDY=row['Loại đào tạo'],
                    CLASSIFIED_BY_ACADEMIC_RECORDS=row['Xếp loại'],
                    CERTIFICATE_NUMBER=row['Số hiệu văn bằng'],
                    NUMBER_ENTERED_INTO_THE_DEGREE_TRACKING_BOOK=row['Số vào sổ'],
                    DATE_OF_DECISION_ANNOUNCEMENT=pd.to_datetime(row['Ngày tốt nghiệp']).date(),
                    COMMENT=row['Ghi chú'],
                    user=user,
                    APPROVED=True
                ))
            except student.DoesNotExist:
                errors.append({"row": index, "error": f"Student ID {row['Mã sinh viên']} không tồn tại"})
            except academic_program.DoesNotExist:
                errors.append({"row": index, "error": f"Academic program '{row['Chuyên ngành đào tạo']}' không tồn tại"})
            except ValidationError as e:
                errors.append({"row": index, "error": f"Validation error: {e}"})
            except Exception as e:
                errors.append({"row": index, "error": f"Error processing row: {str(e)}"})

        # Nếu có lỗi, trả về các lỗi này
        if errors:
            return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)

        # Nếu không có lỗi, thêm tất cả dữ liệu hợp lệ vào cơ sở dữ liệu
        try:
            with transaction.atomic():
                for diploma in valid_data:
                    diploma.save()
        except IntegrityError as e:
            return Response({"error": f"Integrity error: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"Error saving diploma: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"success": "Thêm hồ sơ bằng thành công "}, status=status.HTTP_201_CREATED)