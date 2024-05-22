from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
import pytest

class GlobalSetupTestCase(TestCase):
    def setUp(self):
        # Create a user for diploma_management_profile foreign key
        self.user = User.objects.create_user(username='admin', password='12345678')
        # Create instances of academic_level_type
        academic_level_type.objects.create(
            ACADEMIC_LEVEL_TYPE_ID= 1,
            ACADEMIC_LEVEL_TYPE_NAME='Đại học'
            )
        academic_level_type.objects.create(ACADEMIC_LEVEL_TYPE_NAME='Cao đẳng')
        # Create instances of degree
        degree.objects.create(
            DEGREE_ID = 1,
            DEGREE_NAME='Kỹ thuật Phần mềm', 
            DEGREE_CODE='7480103', 
            DEGREE_STATUS=True, 
            DESCRIPTION='Ngành kỹ thuật Phần mềm'
        )
        # Create instances of academic_program
        academic_program.objects.create(
            ACADEMIC_PROGRAM_ID=1,
            ACADEMIC_PROGRAM_CODE='102',
            ACADEMIC_PROGRAM_NAME='Công nghệ Phần mềm (Đạt kiểm định ABET)',
            MODE_OF_STUDY='Chính quy',
            DEGREE_DURATION='4 Năm',
            DESCRIPTION='Software Engineering',
            ACADEMIC_LEVEL_TYPE_ID=academic_level_type.objects.first(),
            DEGREE_ID=degree.objects.first()
        )
        # Create instances of curriculum
        curriculum.objects.create(
            CURRICULUM_ID = 1,
            CURRICULUM_NAME='K26_CMU_TPM',
            DESCRIPTION='Công nghệ Phần mềm',
            CURRICULUM_STATUS_NAME=True,
            ACADEMIC_PROGRAM_ID=academic_program.objects.first()
        )
        # Create instances of academic_intake_session
        academic_intake_session.objects.create(
            ACADEMIC_INTAKE_SESSION_ID = 1,
            ACADEMIC_INTAKE_SESSION_NAME='Kỳ tuyển sinh 2020-2021',
            START_DATE='2020-10-10'
        )
        academic_intake_session.objects.create(
            ACADEMIC_INTAKE_SESSION_ID = 2,
            ACADEMIC_INTAKE_SESSION_NAME='Kỳ tuyển sinh 2021-2022',
            START_DATE='2021-10-10'
        )
        # Create instances of academic_intake_session_academic_program_curriculum
        academic_intake_session_academic_program_curriculum.objects.create(
            id=1,
            ACADEMIC_INTAKE_SESSION_ID=academic_intake_session.objects.first(),
            ACADEMIC_PROGRAM_ID=academic_program.objects.first(),
            CURRICULUM_ID=curriculum.objects.first(),
            STATUS_NAME=True
        )
        # Create instances of learning_status_type
        learning_status_type.objects.create(
            LEARNING_STATUS_TYPE_ID = 1,
            LEARNING_STATUS_TYPE_NAME='Đang học'
        )
        learning_status_type.objects.create(
             LEARNING_STATUS_TYPE_ID = 2,
            LEARNING_STATUS_TYPE_NAME='Đã hoàn thành'
        )
        # Create instances of student
        student.objects.create(
            STUDENT_ID_NUMBER='26211220570',
            LAST_NAME='Lê',
            FIRST_NAME='Tiến',
            MIDDLE_NAME='Văn',
            GENDER=True,
            BIRTH_DATE='2002-03-25',
            BIRTH_PLACE='Quảng Bình',
            PEOPLE_ID_NUMBER='127364873',
            NATION='Kinh',
            NATIONALITY='Việt Nam',
            PHONE_NUMBER='1234567890',
            EMAIL='levantien@example.com',
            COMMENTS='No comments',
            LEARNING_STATUS_TYPE_ID=learning_status_type.objects.first(),
            ACADEMIC_LEVEL_TYPE_ID=academic_level_type.objects.first()
        )
        # Create instances of student_academic_intake_session_academic_program
        student_academic_intake_session_academic_program.objects.create(
            id = 1,
            STUDENT_ID_NUMBER=student.objects.first(),
            ACADEMIC_INTAKE_SESSION_ID=academic_intake_session.objects.first(),
            ACADEMIC_PROGRAM_ID=academic_program.objects.first(),
            LEARNING_STATUS_TYPE_ID=learning_status_type.objects.first()
        )
        # Create instances of diploma_management_profile
        diploma_management_profile.objects.create(
            DIPLOMA_MANAGEMENT_PROFILE_ID = 1,
            STUDENT_ID_NUMBER=student.objects.first(),
            ACADEMIC_PROGRAM_ID=academic_program.objects.first(),
            GRADUATION_YEAR='2024',
            MODE_OF_STUDY='Chính quy',
            CLASSIFIED_BY_ACADEMIC_RECORDS='Giỏi',
            CERTIFICATE_NUMBER='123433',
            NUMBER_ENTERED_INTO_THE_DEGREE_TRACKING_BOOK='25032002',
            DATE_OF_DECISION_ANNOUNCEMENT='2024-05-01',
            COMMENT='No comment',
            DATE_UPDATED='2024-05-01',
            user=self.user,
            APPROVED=True
        ) 
        refresh = RefreshToken.for_user(self.user)
        # Initialize API client
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')



# ################# Degree Test Cases #################
class DegreeTests(GlobalSetupTestCase):
    def test_get_degree(self):
        url = reverse('degree-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_degree(self):
        data = {
            "DEGREE_NAME": "Khoa học máy tính",
            "DEGREE_CODE": "7480101",
            "DEGREE_STATUS": True,
            "DESCRIPTION": 'Ngành kỹ thuật Phần mềm'
        }
        url = reverse('degree-list')
        response = self.client.post(url,data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_degree_by_id(self):
        response = self.client.get(reverse('degree-id', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_degree(self):
        data = {
            "DEGREE_NAME": 'Kỹ thuật Phần mềm', 
            "DEGREE_CODE" : '7480103', 
            "DEGREE_STATUS" : True, 
            "DESCRIPTION": 'Ngành kỹ thuật Phần mềm'
        }
        response = self.client.put(reverse('degree-id', kwargs={'pk': 1}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_degree(self):
        response = self.client.delete(reverse('degree-id', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

################# Academic Program Cases #################
class AcademicProgramTests(GlobalSetupTestCase):
    def test_get_academic_program(self):
        url = reverse('academic-program-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_academic_program(self):
        data = {
            "ACADEMIC_PROGRAM_CODE": "102",
            "ACADEMIC_PROGRAM_NAME": "Công nghệ Phần mềm (Đạt kiểm định ABET)",
            "MODE_OF_STUDY": "Chính Quy",
            "DEGREE_DURATION": "4 năm",
            "DESCRIPTION": "b",
            "ACADEMIC_LEVEL_TYPE_ID": 1,
            "DEGREE_ID": 1
        }
        url = reverse('academic-program-list')
        response = self.client.post(url,data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_academic_program_by_id(self):
        response = self.client.get(reverse('academic-program-id', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_academic_program(self):
        data = {
            "ACADEMIC_PROGRAM_CODE": "102",
            "ACADEMIC_PROGRAM_NAME": "Công nghệ Phần mềm (Đạt kiểm định ABET)",
            "MODE_OF_STUDY": "Chính Quy",
            "DEGREE_DURATION": "4 năm",
            "DESCRIPTION": "LEVANTIEN",
            "ACADEMIC_LEVEL_TYPE_ID": 1,
            "DEGREE_ID": 1
        }
        response = self.client.put(reverse('academic-program-id', kwargs={'pk': 1}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_academic_program(self):
        response = self.client.delete(reverse('academic-program-id', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


# ################# Curriculum Test Cases #################
class CurriculumTests(GlobalSetupTestCase):
    def test_get_curriculum(self):
        url = reverse('curriculum-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_curriculum(self):
        data = {
            "CURRICULUM_NAME" : 'K26_CMU_TPM',
            "DESCRIPTION" : 'Công nghệ Phần mềm',
            "CURRICULUM_STATUS_NAME" : True,
            "ACADEMIC_PROGRAM_ID":1
        }
        url = reverse('curriculum-list')
        response = self.client.post(url,data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_curriculume_by_id(self):
        response = self.client.get(reverse('curriculum-id', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_curriculum(self):
        data = {
            "CURRICULUM_NAME" : 'K26_CMU_TPM',
            "DESCRIPTION" : 'Công nghệ Phần mềm 1',
            "CURRICULUM_STATUS_NAME" : True,
            "ACADEMIC_PROGRAM_ID":1
        }
        response = self.client.put(reverse('curriculum-id', kwargs={'pk': 1}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_curriculum(self):
        response = self.client.delete(reverse('curriculum-id', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


# ################# Academic Intake Session Test Cases #################
class AcademicIntakeSessionTests(GlobalSetupTestCase):
    def test_get_academic_intake_session(self):
        url = reverse('academic-intake-session-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_academic_intake_session(self):
        data = {
            "ACADEMIC_INTAKE_SESSION_NAME" : 'Kỳ tuyển sinh 2021-2022',
            "START_DATE":'2021-10-10'
        }
        url = reverse('academic-intake-session-list')
        response = self.client.post(url,data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_academic_intake_session_by_id(self):
        response = self.client.get(reverse('academic-intake-session-id', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_academic_intake_session(self):
        data = {
            "ACADEMIC_INTAKE_SESSION_NAME" : 'Kỳ tuyển sinh 2021-2022',
            "START_DATE":'2021-10-11'
        }
        response = self.client.put(reverse('academic-intake-session-id', kwargs={'pk': 1}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_academic_intake_session(self):
        response = self.client.delete(reverse('academic-intake-session-id', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

# ################# Student Test Cases #################
class StudentTests(GlobalSetupTestCase):
    def test_get_student(self):
        url = reverse('student-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_student(self):
        data = {
            "STUDENT_ID_NUMBER":"26211220571",
            "LAST_NAME":"Lê",
            "FIRST_NAME":"Tiến",
            "MIDDLE_NAME":"Văn",
            "GENDER":True,
            "BIRTH_DATE":"2002-03-25",
            "BIRTH_PLACE":"Quảng Bình",
            "PEOPLE_ID_NUMBER":"127364873",
            "NATION":"Kinh",
            "NATIONALITY":"Việt Nam",
            "PHONE_NUMBER":"1234567890",
            "EMAIL":"levantien@example.com",
            "COMMENTS":"No comments",
            "LEARNING_STATUS_TYPE_ID":1,
            "ACADEMIC_LEVEL_TYPE_ID":1
        }
        url = reverse('student-list')
        response = self.client.post(url,data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_student_by_id(self):
        response = self.client.get(reverse('student-id', kwargs={'pk': "26211220570"}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_student(self):
        data = {
            "STUDENT_ID_NUMBER":'26211220570',
            "LAST_NAME":'Lê',
            'FIRST_NAME':'Tiến',
            'MIDDLE_NAME':'Văn',
            'GENDER':False,
            'BIRTH_DATE':'2002-03-25',
            'BIRTH_PLACE':'Quảng Bình',
            'PEOPLE_ID_NUMBER':'127364873',
            'NATION':'Kinh',
            'NATIONALITY':'Việt Nam',
            'PHONE_NUMBER':'1234567890',
            'EMAIL':'levantien@example.com',
            'COMMENTS':'No comments',
            'LEARNING_STATUS_TYPE_ID':1,
            'ACADEMIC_LEVEL_TYPE_ID':1
        }
        response = self.client.put(reverse('student-id', kwargs={'pk': "26211220570"}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_delete_student(self):
        response = self.client.delete(reverse('student-id', kwargs={'pk': "26211220570"}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


# ####   academic_intake_session_academic_program_curriculum   #####
class AISAPCTests(GlobalSetupTestCase):
    def test_get_AISAPC(self):
        url = reverse('AISAPC-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_AISAPC(self):
        data = {
            "id":10,
            "ACADEMIC_INTAKE_SESSION_ID":2,
            "ACADEMIC_PROGRAM_ID":1,
            "CURRICULUM_ID": 1,
            "STATUS_NAME": True
        }
        url = reverse('AISAPC-list')
        response = self.client.post(url,data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_AISAPC_by_id(self):
        response = self.client.get(reverse('AISAPC-id', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_AISAPC(self):
        data = {
            "ACADEMIC_INTAKE_SESSION_ID":2,
            "ACADEMIC_PROGRAM_ID":1,
            "CURRICULUM_ID": 1,
            "STATUS_NAME": True
        }
        response = self.client.put(reverse('AISAPC-id', kwargs={'pk': 1}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_delete_AISAPC(self):
        response = self.client.delete(reverse('AISAPC-id', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


# ####   student_academic_intake_session_academic_program   #####
class SAISAPTests(GlobalSetupTestCase):
    def test_get_SAISAP(self):
        url = reverse('SAISAP-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_SAISAP(self):
        data = {
            "ACADEMIC_INTAKE_SESSION_ID":2,
            "ACADEMIC_PROGRAM_ID":1,
            "STUDENT_ID_NUMBER": "26211220570",
            "LEARNING_STATUS_TYPE_ID": 1
        }
        url = reverse('SAISAP-list')
        response = self.client.post(url,data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_SAISAP_by_id(self):
        response = self.client.get(reverse('SAISAP-id', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_SAISAP(self):
        data = {
            "ACADEMIC_INTAKE_SESSION_ID":1,
            "ACADEMIC_PROGRAM_ID":1,
            "STUDENT_ID_NUMBER": "26211220570",
            "LEARNING_STATUS_TYPE_ID": 1
        }
        response = self.client.put(reverse('SAISAP-id', kwargs={'pk': 1}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_delete_SAISAP(self):
        response = self.client.delete(reverse('SAISAP-id', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class DiplomaTests(GlobalSetupTestCase):
    def test_get_Diploma(self):
        url = reverse('Diploma-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_create_Diploma(self):
    #     data = {
    #         "DIPLOMA_MANAGEMENT_PROFILE_ID" : 1,
    #         "STUDENT_ID_NUMBER" : "26211220570",
    #         "ACADEMIC_PROGRAM_ID":1,
    #         "GRADUATION_YEAR":'2024',
    #         "MODE_OF_STUDY" : "Chính quy",
    #         "CLASSIFIED_BY_ACADEMIC_RECORDS":'Giỏi',
    #         "CERTIFICATE_NUMBER":'123433',
    #         "NUMBER_ENTERED_INTO_THE_DEGREE_TRACKING_BOOK":'25032002',
    #         "DATE_OF_DECISION_ANNOUNCEMENT":'2024-05-01',
    #         "COMMENT":'No comment',
    #         "DATE_UPDATED":'2024-05-01',
    #         # "user":self.user,
    #         "APPROVED":True
    #     }
    #     url = reverse('Diploma-list')
    #     response = self.client.post(url,data, format='json')
    #     print(response.data)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_Diploma_by_id(self):
        response = self.client.get(reverse('Diploma-id', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_update_Diploma(self):
    #     data = {
    #         "DIPLOMA_MANAGEMENT_PROFILE_ID" : 1,
    #         "STUDENT_ID_NUMBER" : "26211220570",
    #         "ACADEMIC_PROGRAM_ID":1,
    #         "GRADUATION_YEAR":'2024',
    #         "MODE_OF_STUDY" : "Chính quy",
    #         "CLASSIFIED_BY_ACADEMIC_RECORDS":'Giỏi',
    #         "CERTIFICATE_NUMBER":'123433',
    #         "NUMBER_ENTERED_INTO_THE_DEGREE_TRACKING_BOOK":'25032002',
    #         "DATE_OF_DECISION_ANNOUNCEMENT":'2024-05-01',
    #         "COMMENT":'No comment',
    #         "DATE_UPDATED":'2024-05-01',
    #         # "user":self.user,
    #         "APPROVED":True
    #     }
    #     response = self.client.put(reverse('Diploma-id', kwargs={'pk': 1}), data, format='json')
    #     print(response.data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_delete_Diploma(self):
        response = self.client.delete(reverse('Diploma-id', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
