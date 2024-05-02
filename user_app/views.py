from rest_framework.views import APIView
from rest_framework.response import Response
from captcha.helpers import captcha_image_url
from captcha.models import CaptchaStore
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist

from admin_app.models import *
from .serializers import *


class GenerateCaptchaAPIView(APIView):
    def get(self, request):
        # Generate a new CAPTCHA key
        captcha_key = CaptchaStore.generate_key()
        
        # Generate the image URL using the captcha_key
        image_url = captcha_image_url(captcha_key)

        # Serialize the key and image URL into JSON format
        captcha_data = {
            'key': captcha_key,
            'image_url': image_url
        }

        # Return the serialized data as a JSON response
        return Response(captcha_data)
    

class InformationRetrievalthroughTextAPIView(APIView):
    def post(self, request):
        student_name = request.data.get('STUDENT_NAME')
        certificate_number= request.data.get('CERTIFICATE_NUMBER')
        captcha_key = request.data.get('CAPTCHA_KEY')
        captcha_response = request.data.get('CAPTCHA_RESPONSE').lower()
        number_entered_into_the_degree_tracking_book = request.data.get('NUMBER_ENTERED_INTO_THE_DEGREE_TRACKING_BOOK')

        if not (student_name ):
            return Response({"Message": "STUDENT_NAME is required.","errCode":"-1"}, status=status.HTTP_400_BAD_REQUEST)
        if not (certificate_number):
            return Response({"Message": "CERTIFICATE_NUMBER is required.","errCode":"-1"}, status=status.HTTP_400_BAD_REQUEST)
        if not (captcha_key):
            return Response({"Message": "CAPTCHA_KEY is required.","errCode":"-1"}, status=status.HTTP_400_BAD_REQUEST)
        if not (captcha_response):
            return Response({"Message": "CAPTCHA_RESPONSE is required.","errCode":"-1"}, status=status.HTTP_400_BAD_REQUEST)
        if not (number_entered_into_the_degree_tracking_book):
            return Response({"Message": "NUMBER_ENTERED_INTO_THE_DEGREE_TRACKING_BOOK is required.","errCode":"-1"}, status=status.HTTP_400_BAD_REQUEST)


        try:
            captcha = CaptchaStore.objects.get(hashkey=captcha_key)
            if captcha.response == captcha_response:
                # Tách tên sinh viên thành first_name, last_name và middle_name
                parts = student_name.split()
                if len(parts) == 3:
                    last_name, middle_name, first_name  = parts
                elif len(parts) == 2:
                    first_name, last_name = parts
                    middle_name = ''
                else:
                    return Response({'error': 'Invalid student name format. Please provide full name ',"errCode":"-1"}, status=status.HTTP_400_BAD_REQUEST)
                try:
                    # Sử dụng phương thức get() để lấy một đối tượng duy nhất từ cơ sở dữ liệu
                    # Nếu không có đối tượng nào hoặc có nhiều hơn một đối tượng thỏa mãn điều kiện, sẽ ném ra ngoại lệ
                    diplopma_profile = diploma_management_profile.objects.get(LAST_NAME=last_name, 
                                                                    MIDDLE_NAME=middle_name, 
                                                                    FIRST_NAME=first_name, 
                                                                    CERTIFICATE_NUMBER=certificate_number)
                    serializer = DiplomaManagementProfileSerializer(diplopma_profile)
                    return Response({"data": serializer.data, "message": "Tìm kiếm thành công","errCode":"0"},status=status.HTTP_200_OK)
                except diploma_management_profile.DoesNotExist:
                    # Trả về thông báo lỗi nếu không tìm thấy đối tượng
                    return Response({"message": "Không tìm thấy hồ sơ phù hợp.","errCode":"0"}, status=status.HTTP_404_NOT_FOUND)
                except Exception as e:
                    # Trả về thông báo lỗi chung nếu có lỗi xảy ra
                    return Response({"message": "Đã xảy ra lỗi khi xử lý yêu cầu.","errCode":"1"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                # Xác thực không thành công
                return Response({'message': 'Captcha không đúng',"captcha_response": captcha.response}, status=status.HTTP_400_BAD_REQUEST)
        except CaptchaStore.DoesNotExist:
            # Nếu không tìm thấy CAPTCHA key
            return Response({'success': False, 'error': 'Invalid CAPTCHA key.'}, status=400)