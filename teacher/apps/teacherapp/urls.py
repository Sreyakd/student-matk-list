from django.urls import path
from apps.teacherapp import views

urlpatterns = [
    path("teacher_create_update",views.TeacherDetailsCreateOrUpdateApiView.as_view()),
    path("teacher_detail",views.GetAllTeacherDetails.as_view()),
    path("teacher_detail_delete",views.TeacherDetailsDelete.as_view())
]