from django.urls import path
from apps.student import views
urlpatterns = [
    path('register/',views.StudentDetailsCreateOrUpdateApiView.as_view()),
    path('list',views.GetAllUsertDetails.as_view()),
    path('remove',views.UserDetailsDelete.as_view())
]