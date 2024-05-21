from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from .models import *
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User



##### Global Set Up to Test  #############
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from django.test import TestCase
from .models import (
    academic_level_type, degree, academic_program, curriculum,
    academic_intake_session, learning_status_type, student,
    student_academic_intake_session_academic_program, diploma_management_profile
)

class GlobalSetupTestCase(TestCase):
    def setUp(self):
        # Create a user for diploma_management_profile foreign key
        self.user = User.objects.create_user(username='admin', password='password')

        # Create instances of academic_level_type
        undergraduate = academic_level_type.objects.create(ACADEMIC_LEVEL_TYPE_NAME='Đại học')
        college = academic_level_type.objects.create(ACADEMIC_LEVEL_TYPE_NAME='Cao đẳng')
        master = academic_level_type.objects.create(ACADEMIC_LEVEL_TYPE_NAME='Thạc sĩ')

        # Create instances of degree
        software_engineering = degree.objects.create(DEGREE_NAME='Kỹ thuật Phần mềm', DEGREE_CODE='7480103', DEGREE_STATUS='True', DESCRIPTION='Ngành kỹ thuật Phần mềm')
        information_security = degree.objects.create(DEGREE_NAME='An toàn Thông tin', DEGREE_CODE='7480202', DEGREE_STATUS='True', DESCRIPTION='Ngành an Toàn thông tin')

        # Create instances of academic_program
        software_eng_program = academic_program.objects.create(
            ACADEMIC_PROGRAM_CODE='102',
            ACADEMIC_PROGRAM_NAME='Công nghệ Phần mềm (Đạt kiểm định ABET)',
            MODE_OF_STUDY='Chính quy',
            DEGREE_DURATION='4 Năm',
            DESCRIPTION='Software Engineering',
            ACADEMIC_LEVEL_TYPE=undergraduate,
            DEGREE=software_engineering
        )
        info_sec_program = academic_program.objects.create(
            ACADEMIC_PROGRAM_CODE='124',
            ACADEMIC_PROGRAM_NAME='An toàn Thông tin',
            MODE_OF_STUDY='Chính quy',
            DEGREE_DURATION='4 Năm',
            DESCRIPTION='An toàn thông tin',
            ACADEMIC_LEVEL_TYPE=undergraduate,
            DEGREE=information_security
        )

        # Create instances of curriculum
        curriculum.objects.create(
            CURRICULUM_NAME='K20_CMU_TPM',
            DESCRIPTION='Công nghệ Phần mềm',
            CURRICULUM_STATUS_NAME=True,
            ACADEMIC_PROGRAM=software_eng_program
        )
        curriculum.objects.create(
            CURRICULUM_NAME='K26_CMU_TPM',
            DESCRIPTION='Công nghệ Phần mềm',
            CURRICULUM_STATUS_NAME=True,
            ACADEMIC_PROGRAM=software_eng_program
        )

        # Create instances of academic_intake_session
        academic_intake_session.objects.create(
            ACADEMIC_INTAKE_SESSION_NAME='Kỳ tuyển sinh 2020-2021',
            START_DATE='2020-10-10'
        )
        academic_intake_session.objects.create(
            ACADEMIC_INTAKE_SESSION_NAME='Kỳ tuyển sinh 2021-2022',
            START_DATE='2021-10-10'
        )

        # Create instances of learning_status_type
        learning_status_type.objects.create(
            LEARNING_STATUS_TYPE_NAME='Đang học'
        )
        learning_status_type.objects.create(
            LEARNING_STATUS_TYPE_NAME='Đã hoàn thành'
        )
        learning_status_type.objects.create(
            LEARNING_STATUS_TYPE_NAME='Bị thôi học'
        )

        # Create instances of student
        student1 = student.objects.create(
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
            LEARNING_STATUS_TYPE=learning_status_type.objects.get(LEARNING_STATUS_TYPE_NAME='Đang học'),
            ACADEMIC_LEVEL_TYPE=undergraduate
        )
        student2 = student.objects.create(
            STUDENT_ID_NUMBER='26211220560',
            LAST_NAME='Nguyễn',
            FIRST_NAME='Bảo',
            MIDDLE_NAME='Văn',
            GENDER=True,
            BIRTH_DATE='2002-03-25',
            BIRTH_PLACE='Quảng Nam',
            PEOPLE_ID_NUMBER='127364873',
            NATION='Kinh',
            NATIONALITY='Việt Nam',
            PHONE_NUMBER='1234567890',
            EMAIL='nguyenvanbao@example.com',
            COMMENTS='No comments',
            LEARNING_STATUS_TYPE=learning_status_type.objects.get(LEARNING_STATUS_TYPE_NAME='Đang học'),
            ACADEMIC_LEVEL_TYPE=undergraduate
        )

        # Create instances of student_academic_intake_session_academic_program
        student_academic_intake_session_academic_program.objects.create(
            STUDENT=student1,
            ACADEMIC_INTAKE_SESSION=academic_intake_session.objects.get(ACADEMIC_INTAKE_SESSION_NAME='Kỳ tuyển sinh 2020-2021'),
            ACADEMIC_PROGRAM=software_eng_program,
            LEARNING_STATUS_TYPE=learning_status_type.objects.get(LEARNING_STATUS_TYPE_NAME='Đang học')
        )
        student_academic_intake_session_academic_program.objects.create(
            STUDENT=student2,
            ACADEMIC_INTAKE_SESSION=academic_intake_session.objects.get(ACADEMIC_INTAKE_SESSION_NAME='Kỳ tuyển sinh 2020-2021'),
            ACADEMIC_PROGRAM=software_eng_program,
            LEARNING_STATUS_TYPE=learning_status_type.objects.get(LEARNING_STATUS_TYPE_NAME='Đang học')
        )

        # Create instances of diploma_management_profile
        diploma_management_profile.objects.create(
            STUDENT=student1,
            ACADEMIC_PROGRAM=software_eng_program,
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

        # The app uses token authentication
        self.token = Token.objects.create(user=self.user)

        # Initialize API client
        self.client = APIClient()

        # Pass the token in all calls to the API
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)




################# Test Cases #################
class DegreeTests(GlobalSetupTestCase):
    def test_create_degree(self):
        data = {
            "DEGREE_NAME": "Khoa học máy tính",
            "DEGREE_CODE": "7480101",
            "DEGREE_STATUS": True
        }
        response = self.client.post('/degree', format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(degree.objects.count(), 3)
    # def test_get_academic_program(self):
    #     response = self.client.get(reverse('academic_program-detail', kwargs={'pk': self.academic_program.pk}))
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertContains(response, self.academic_program.ACADEMIC_PROGRAM_NAME)

    # def test_update_academic_program(self):
    #     data = {
    #         'ACADEMIC_PROGRAM_CODE': 'CS102',
    #         'ACADEMIC_PROGRAM_NAME': 'Updated Computer Science',
    #         'MODE_OF_STUDY': 'Full-time',
    #         'DEGREE_DURATION': '4 years',
    #         'DESCRIPTION': 'Updated Computer Science Program',
    #         'ACADEMIC_LEVEL_TYPE_ID': self.academic_level_type.pk,
    #         'DEGREE_ID': self.degree.pk
    #     }
    #     response = self.client.put(reverse('academic_program-detail', kwargs={'pk': self.academic_program.pk}), data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_delete_academic_program(self):
    #     response = self.client.delete(reverse('academic_program-detail', kwargs={'pk': self.academic_program.pk}))
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)