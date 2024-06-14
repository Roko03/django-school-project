from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns =  [
    path('',views.home,name='home'),
    path('signup/',views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    
    path('admin_page/',views.admin, name='admin_page'),
    path('admin_page/user_form/',views.addUser, name='admin_user_form'),
    path('admin_page/user_form_update/<str:pk>',views.editUser, name='admin_user_form_update'),

    path('admin_page/subject/',views.subject, name='admin_subject'),
    path('admin_page/subject_detail/<str:pk>/',views.subject_detail, name='admin_subject_detail'),
    path('admin_page/subject_form/',views.createSubject, name='admin_create_subject'),
    path('admin_page/subject_update/<str:pk>/',views.updateSubject, name='admin_subject_update'),
    path('admin_page/subject_delete/<str:pk>/',views.deleteSubject, name='admin_subject_delete'),

    path('admin_page/student/', views.student, name='admin_student'),
    path('admin_page/student_update/<str:pk>',views.updateStudent, name='admin_student_update'),
    path('admin_page/student_delete/<str:pk>/',views.deleteStudent, name='admin_student_delete'),

    path('admin_page/professor/', views.professor, name='admin_professor'),
    path('admin_page/professor_update/<str:pk>', views.updateProfessor, name='admin_professor_update'),
    path('admin_page/professor_delete/<str:pk>', views.deleteProfessor, name='admin_professor_delete'),

    path('admin_page/upisi/', views.upisi, name='admin_upisi'),
    path('admin_page/upisi_delete/<str:pk>', views.deleteUpis, name='admin_upisi_delete'),

    path('professor/', views.professor_page, name='professor'),
    path('professor/subject', views.professor_subject, name='professor_subject'),
    path('professor/students', views.professor_students, name='professor_students'),
    path('professor/student_update/<str:pk>', views.professor_student_update, name='professor_student_update'),
   
    path('subject/', views.student_subject, name='subject'),
    path('subject_upis/<str:pk>', views.subject_upis, name='subject_upis'),

]