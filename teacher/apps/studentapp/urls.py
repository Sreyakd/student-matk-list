from django.urls import path
from apps.studentapp import views

urlpatterns = [
    path('create_update',views.StudentDetailsCreateOrUpdateApiView.as_view()),
    path('get_student_details',views.GetAllStudentDetails.as_view()),
    path('active_or_inactive',views.ActiveOrInactiveView.as_view()),
    path('student_details_delete',views.StudentDetailsDelete.as_view())
]