from rest_framework.views import APIView
from rest_framework.response import Response
from captcha.helpers import captcha_image_url
from captcha.models import CaptchaStore
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist

from PIL import Image
from io import BytesIO
import cv2
from django.core.files.uploadedfile import InMemoryUploadedFile
import numpy as np
import pytesseract

from admin_app.models import *
from .serializers import *

pytesseract.pytesseract.tesseract_cmd = r"C:\Users\lvtie\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

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
                ## Tách tên sinh viên thành first_name, last_name và middle_name
                parts = student_name.split()
                if len(parts) == 3:
                    last_name, middle_name, first_name  = parts
                else:
                    return Response({'error': 'Invalid student name format. Please provide full name ',"errCode":"-1"}, status=status.HTTP_400_BAD_REQUEST)
                
                #### Lấy thông tin section
                try:
                    ## Sử dụng phương thức get() để lấy một đối tượng duy nhất từ cơ sở dữ liệu
                    diplopma_profile = diploma_management_profile.objects.get( 
                                                                    CERTIFICATE_NUMBER=certificate_number,
                                                                    NUMBER_ENTERED_INTO_THE_DEGREE_TRACKING_BOOK = number_entered_into_the_degree_tracking_book)
                    student_information = student.objects.get(STUDENT_ID_NUMBER=diplopma_profile.STUDENT_ID_NUMBER)

                    if student_information.LAST_NAME != last_name or student_information.FIRST_NAME != first_name or student_information.MIDDLE_NAME != middle_name:
                        return Response({"message": "Không tìm thấy hồ sơ phù hợp!","errCode":"-1"}, status=status.HTTP_400_BAD_REQUEST)
                    serializer = DiplomaManagementProfileSerializer(diplopma_profile)
                    return Response({"data": serializer.data, "message": "Tìm kiếm thành công!","errCode":"0"},status=status.HTTP_200_OK)
                ## Nếu không có đối tượng nào hoặc có nhiều hơn một đối tượng thỏa mãn điều kiện, sẽ ném ra ngoại lệ
                except diploma_management_profile.DoesNotExist:
                    # Trả về thông báo lỗi nếu không tìm thấy đối tượng
                    return Response({"message": "Không tìm thấy hồ sơ phù hợp!","errCode":"0"}, status=status.HTTP_404_NOT_FOUND)
                except Exception as e:
                    # Trả về thông báo lỗi chung nếu có lỗi xảy ra
                    return Response({"message": "Đã xảy ra lỗi khi xử lý yêu cầu!","errCode":"1"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                # Xác thực không thành công
                return Response({"message": "Captcha không đúng!","errCode":"-1"}, status=status.HTTP_400_BAD_REQUEST)
        except CaptchaStore.DoesNotExist:
            # Nếu không tìm thấy CAPTCHA key
            return Response({"message": "Invalid CAPTCHA key" ,"errCode":"-1"}, status=status.HTTP_400_BAD_REQUEST)
        



####################################################################
###################### Image Processing ############################
####################################################################
#### Cân Bằng Trắng (White Balancing):
def white_balance(image):
    result = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    avg_a = np.average(result[:, :, 1])
    avg_b = np.average(result[:, :, 2])
    result[:, :, 1] = result[:, :, 1] - ((avg_a - 128) * (result[:, :, 0] / 255.0) * 1.1)
    result[:, :, 2] = result[:, :, 2] - ((avg_b - 128) * (result[:, :, 0] / 255.0) * 1.1)
    return cv2.cvtColor(result, cv2.COLOR_LAB2BGR)
#### Lọc Gaussian (Gaussian Blurring)
def gaussian_blur(image):
    return cv2.GaussianBlur(image, (5, 5), 0)

##### Resize for Student Name
def resize_student_name_image_for_tesseract(image):
    height, width = image.shape[:2]
    scale_factor = min(800 / width, 600 / height)
    # Tính toán kích thước mới dựa trên tỷ lệ này
    new_width = int(width * scale_factor)
    new_height = int(height * scale_factor)
    # Thay đổi kích thước hình ảnh theo kích thước đã tính toán
    resized_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_LINEAR)
    return resized_image

###### Resize for Number
def resize_number_image_for_tesseract(image):
    height, width = image.shape[:2]
    scale_factor = min(650 / width, 400 / height)
    # Tính toán kích thước mới dựa trên tỷ lệ này
    new_width = int(width * scale_factor)
    new_height = int(height * scale_factor)
    # Thay đổi kích thước hình ảnh theo kích thước đã tính toán
    resized_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_LINEAR)
    return resized_image

def read_image_from_upload(file: InMemoryUploadedFile):
    image_data = file.read()
    nparr = np.frombuffer(image_data, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return image

def extract_regions_of_interest(image):
    height, width = image.shape[:2]
    # Cắt giữa phần bên phải và phần dưới góc trái của phần bên phải

    #giữa phần bên phải chiếm 1/2 chiều rộng bên phải của ảnh, từ 1/4 đến 3/4 chiều cao
    mid_right_x_start = int(width / 2)
    mid_right_y_start = int(height / 3)
    mid_right_x_end = width
    mid_right_y_end = int(2 * height / 3)
    mid_right = image[mid_right_y_start:mid_right_y_end, mid_right_x_start:mid_right_x_end]

    # Phần dưới góc trái của phần bên phải chiếm 1/4 chiều rộng bên phải và 1/4 chiều cao dưới cùng
    bottom_left_x_start = int(11* width / 20)
    bottom_left_y_start = int(3 * height / 4)

    bottom_left_x_end = int(3 * width / 4)
    bottom_left_y_end = height
    bottom_left = image[bottom_left_y_start:bottom_left_y_end, bottom_left_x_start:bottom_left_x_end]
    return mid_right, bottom_left

def extract_name(text):
    # Tìm dòng chứa từ khóa "Cho:"
    lines = text.split('\n')
    for line in lines:
        if "Ông" in line:
            # Tách tên sau "Cho:"
            parts = line.split("Ông")
            if len(parts) > 1:
                name = parts[1].strip()
                return name
    return None

def get_student_name(image):
    image = resize_student_name_image_for_tesseract(image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    text  = pytesseract.image_to_string(gray, lang='vie')
    name = extract_name(text)
    # boxes = pytesseract.image_to_data(gray)
    # for x, b in enumerate(boxes.splitlines()):
    #     if x != 0:
    #         b = b.split()
    #         if len(b) == 12:
    #             x, y, w, h = int(b[6]), int(b[7]), int(b[8]), int(b[9])
    #             cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
    # # Hiển thị ảnh với các bounding boxes
    # cv2.imshow('Result', image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return name

###### CERTIFICATE_NUMBER
def extract_certificate_number(text):
    # Tìm dòng chứa từ khóa "sốhiệu:"
    lines = text.split('\n')
    if len(lines) >= 1:
        for line in lines:
            parts = line.split(' ')
            if len(parts) > 1:
                certificate_number = parts[1]
                return certificate_number
    return None
def get_certificate_number(image):
    image = resize_number_image_for_tesseract(image) 
    # white = white_balance(image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray, lang='vie')
    certificate_number = extract_certificate_number(text)
    # boxes = pytesseract.image_to_data(gray)
    # for x, b in enumerate(boxes.splitlines()):
    #     if x != 0:
    #         b = b.split()
    #         if len(b) == 12:
    #             x, y, w, h = int(b[6]), int(b[7]), int(b[8]), int(b[9])
    #             cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
    # # Hiển thị ảnh với các bounding boxes
    # cv2.imshow('Result', image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return certificate_number

###### NUMBER IN DEGREE
def extract_number_in_degree(text):
    # Tìm dòng chứa từ khóa "Sốvào sổ cấp bằng:"
    lines = text.split('\n')
    for line in lines:
        if "Số vào sổ cấp bằng" in line:
            parts = line.split(' ')
            if len(parts) > 1:
                number_in_degree = parts[-1]
                return number_in_degree
    return None
def get_number_in_degree(image):
    image = resize_number_image_for_tesseract(image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray, lang='vie')
    number_in_degree = extract_number_in_degree(text)
    # boxes = pytesseract.image_to_data(gray)
    # for x, b in enumerate(boxes.splitlines()):
    #     if x != 0:
    #         b = b.split()
    #         if len(b) == 12:
    #             x, y, w, h = int(b[6]), int(b[7]), int(b[8]), int(b[9])
    #             cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
    # # Hiển thị ảnh với các bounding boxes
    # cv2.imshow('Result', image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return number_in_degree

class InformationRetrievalthroughImageAPIView(APIView):
    def post(self, request):
        post_serializer = ImageUploadSerializer(data=request.data)
        if post_serializer.is_valid():
            uploaded_image = post_serializer.validated_data['image']
            
            ### Sử dụng hàm read_image_from_upload để đọc ảnh từ đối tượng InMemoryUploadedFile để có thể sử dụng với OpenCV
            image = read_image_from_upload(uploaded_image)
            
            ### Lấy các phần ảnh cần sử dụng
            mid_right, bottom_left = extract_regions_of_interest(image)
            student_name = get_student_name(mid_right)
            certificate_number = get_certificate_number(bottom_left)
            number_in_degree = get_number_in_degree(bottom_left)
            print(student_name, certificate_number, number_in_degree)

            ######### kiểm tra xem có extract được text phù hợp không 
            if student_name is None or certificate_number is None or number_in_degree is None:
                return Response({"message": "Lỗi: Vui lòng gử lại ảnh gồm toàn bộ hình ảnh của văn bằng và chất lượng tốt hơn!!!!","errCode":"-1"}, status=status.HTTP_400_BAD_REQUEST)
            
            ######## tách student name thành first_name, last_name và middle_name
            parts = student_name.split()
            if len(parts) == 3:
                last_name, middle_name, first_name  = parts
            else:
                return Response({'error': 'Invalid student name format. Please provide full name ',"errCode":"-1"}, status=status.HTTP_400_BAD_REQUEST)
            
            ###### phần lấy đối tượng và trả về kết quả cho client
            try:
                ## Sử dụng phương thức get() để lấy một đối tượng duy nhất từ cơ sở dữ liệu
                diplopma_profile = diploma_management_profile.objects.get( 
                                                                    CERTIFICATE_NUMBER=certificate_number,
                                                                    NUMBER_ENTERED_INTO_THE_DEGREE_TRACKING_BOOK = number_in_degree)
                student_information = student.objects.get(STUDENT_ID_NUMBER=diplopma_profile.STUDENT_ID_NUMBER)
                if student_information.LAST_NAME != last_name or student_information.FIRST_NAME != first_name or student_information.MIDDLE_NAME != middle_name:
                        return Response({"message": "Không tìm thấy hồ sơ phù hợp!","errCode":"-1"}, status=status.HTTP_400_BAD_REQUEST)
                response_serializer = DiplomaManagementProfileSerializer(diplopma_profile)
                return Response({"data": response_serializer.data, "message": "Tìm kiếm thành công","errCode":"0"},status=status.HTTP_200_OK)
            ## Nếu không có đối tượng nào hoặc có nhiều hơn một đối tượng thỏa mãn điều kiện, sẽ ném ra ngoại lệ
            except diploma_management_profile.DoesNotExist:
                    # Trả về thông báo lỗi nếu không tìm thấy đối tượng
                return Response({"message": "Không tìm thấy hồ sơ phù hợp.","errCode":"0"}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                    # Trả về thông báo lỗi chung nếu có lỗi xảy ra
                return Response({"message": "Đã xảy ra lỗi khi xử lý yêu cầu.","errCode":"1"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"message": "Lỗi: Không có hình ảnh được gửi.","errCode":"-1"}, status=status.HTTP_400_BAD_REQUEST)