from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views import View
from .models import Lesson, Student, Teacher, Attendance, Assignment, Grade
from .serializers import LessonSerializer ,AssignmentSerializer , GradeSerializer
from rest_framework import viewsets


class LessonViewSet(viewsets.ModelViewSet):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class StudentListView(View):
    def get(self, request):
        students = Student.objects.all().values('id', 'name', 'level')
        return JsonResponse(list(students), safe=False)


class StudentDetailView(View):
    def get(self, request, pk):
        student = get_object_or_404(Student, pk=pk)
        data = {
            'id': student.id,
            'name': student.name,
            'level': student.level,
            'classes': list(student.classes.values('course_id', 'title'))
        }
        return JsonResponse(data)


class TeacherListView(View):
    def get(self, request):
        teachers = Teacher.objects.all().values('id', 'name', 'email', 'experience')
        return JsonResponse(list(teachers), safe=False)


class TeacherDetailView(View):
    def get(self, request, pk):
        teacher = get_object_or_404(Teacher, pk=pk)
        data = {
            'id': teacher.id,
            'name': teacher.name,
            'email': teacher.email,
            'experience': teacher.experience,
            'student': teacher.student.name,
            'classes': teacher.classes
        }
        return JsonResponse(data)


class AttendanceListView(View):
        def get(self, request):
            attendances = Attendance.objects.all().values('id', 'student__name', 'lesson__title', 'date', 'status')
            return JsonResponse(list(attendances), safe=False)


class AttendanceDetailView(View):
        def get(self, request, pk):
            attendance = get_object_or_404(Attendance, pk=pk)
            data = {
                'id': attendance.id,
                'student': attendance.student.name,
                'lesson': attendance.lesson.title,
                'date': attendance.date,
                'status': attendance.get_status_display()
            }
            return JsonResponse(data)


class AssignmentViewSet(viewsets.ModelViewSet):
   serializer_class = AssignmentSerializer
   queryset = Assignment.objects.all()


class GradeViewSet(viewsets.ModelViewSet):
    serializer_class = GradeSerializer
    queryset = Grade.objects.all()
