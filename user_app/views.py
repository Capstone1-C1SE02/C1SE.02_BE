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
                elif len(parts) == 2:
                    first_name, last_name = parts
                    middle_name = ''
                else:
                    return Response({'error': 'Invalid student name format. Please provide full name ',"errCode":"-1"}, status=status.HTTP_400_BAD_REQUEST)
                try:
                    ## Sử dụng phương thức get() để lấy một đối tượng duy nhất từ cơ sở dữ liệu
                    diplopma_profile = diploma_management_profile.objects.get(LAST_NAME=last_name, 
                                                                    MIDDLE_NAME=middle_name, 
                                                                    FIRST_NAME=first_name, 
                                                                    CERTIFICATE_NUMBER=certificate_number)
                    serializer = DiplomaManagementProfileSerializer(diplopma_profile)
                    return Response({"data": serializer.data, "message": "Tìm kiếm thành công","errCode":"0"},status=status.HTTP_200_OK)
                ## Nếu không có đối tượng nào hoặc có nhiều hơn một đối tượng thỏa mãn điều kiện, sẽ ném ra ngoại lệ
                except diploma_management_profile.DoesNotExist:
                    # Trả về thông báo lỗi nếu không tìm thấy đối tượng
                    return Response({"message": "Không tìm thấy hồ sơ phù hợp.","errCode":"0"}, status=status.HTTP_404_NOT_FOUND)
                except Exception as e:
                    # Trả về thông báo lỗi chung nếu có lỗi xảy ra
                    return Response({"message": "Đã xảy ra lỗi khi xử lý yêu cầu.","errCode":"1"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                # Xác thực không thành công
                return Response({"message": "Captcha không đúng","errCode":"-1"}, status=status.HTTP_400_BAD_REQUEST)
        except CaptchaStore.DoesNotExist:
            # Nếu không tìm thấy CAPTCHA key
            return Response({"message": "Invalid CAPTCHA key" ,"errCode":"-1"}, status=status.HTTP_400_BAD_REQUEST)
        
def read_image_from_upload(file: InMemoryUploadedFile):
        # Đọc dữ liệu ảnh từ đối tượng InMemoryUploadedFile
        image_data = file.read()
        # Chuyển dữ liệu ảnh thành mảng NumPy
        nparr = np.frombuffer(image_data, np.uint8)
        # Đọc ảnh từ mảng NumPy
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        return image

class InformationRetrievalthroughImageAPIView(APIView):
    def post(self, request):
        serializer = ImageUploadSerializer(data=request.data)
        if serializer.is_valid():
            uploaded_image = serializer.validated_data['image']

            ### Sử dụng hàm read_image_from_upload để đọc ảnh từ đối tượng InMemoryUploadedFile để có thể sử dụng với OpenCV
            image = read_image_from_upload(uploaded_image)

            # # Grayscale, Gaussian blur, Otsu's threshold
            # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            # # blur = cv2.GaussianBlur(gray, (3,3), 0)
            # thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

            # # Morph open to remove noise and invert image
            # # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
            # # opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
            # # invert = 255 - opening

            # # Perform text extraction
            # data = pytesseract.image_to_string(thresh, lang='vie', config='--psm 6')
            # print(data)

            # cv2.imshow('thresh', thresh)
            # # cv2.imshow('opening', opening)
            # # cv2.imshow('invert', invert)
            # cv2.waitKey()
            # cv2.destroyAllWindows()
            # Chuyển ảnh sang ảnh xám
            # gray_image = image_pil.convert('L')

            # Chuyển ảnh xám sang mảng NumPy để sử dụng với OpenCV
            # gray_image_np = np.array(gray_image)


            # # Nhận diện văn bản từ ảnh
            # recognized_text = pytesseract.image_to_string(gray_image_np, lang='vie')

            # print(recognized_text)
            # # Chuyển hình ảnh sang ảnh xám
            image_pil = image.convert('L')
            text =  pytesseract.image_to_string(image_pil,lang='vie')
            print(text)

            # Chuyển ảnh xám sang mảng numpy
            image_np = np.array(image_pil)
            boxes = pytesseract.image_to_data(image_np)
            for x,b in enumerate(boxes.splitlines()):
                if x!=0:
                    b = b.split()
                    # print(b)
                    if len(b) == 12:
                        x,y,w,h = int(b[6]),int(b[7]),int(b[8]),int(b[9])
                        cv2.rectangle(image_np,(x,y),(w+x,h+y),(0,0,255),2)
            cv2.imshow('Result',image_np)
            cv2.waitKey()
            cv2.destroyAllWindows()

            # Nhận diện văn bản từ ảnh
            # text = pytesseract.image_to_string(image_np)
            # Tách thông tin sinh viên từ văn bản
            # print(text)


            return Response({"message": "Hình ảnh đã được nhận thành công.","errCode":"0"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Lỗi: Không có hình ảnh được gửi.","errCode":"-1"}, status=status.HTTP_400_BAD_REQUEST)