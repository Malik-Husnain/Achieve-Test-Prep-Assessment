from django.urls import path
from .views import *

urlpatterns = [
    path('login/', login_view, name='login'),
    path('progress/', progress_view, name='progress'),
    path('logout/', logout_view, name='logout'),
    path('api/courses/', CourseProgressAPIView.as_view(), name='course-progress-api'),
    path('api/recommendations/', BookRecommendationAPIView.as_view(), name='book-recommendations'),
    path('api/progress/add/', AddCourseProgressAPIView.as_view(), name='add_course_progress'),
    
]