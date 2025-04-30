from django.urls import path
from . import views

urlpatterns=[
    path('login',views.admin_login,name='login'),
    path('dashboard',views.dashboard,name="admin-dashboard"),
    path('contact-list',views.contact_list,name="contact-list"),
    path('volunteer-application-list',views.volunteer_list,name="application-list"),
    path('logout',views.admin_logout,name="logout"),  
    path('register',views.admin_register,name='register'),
    path('upload-blog',views.upload_blog,name="upload-blog"),
    path('edit-blog/<int:id>/',views.edit_blog,name="edit-blog"),
    path('delete-blog/<int:id>/',views.deleteBlog,name="delete-blog"),
    path('delete-row/<str:tbl>/<int:id>/',views.deleteRow,name="delete-row"),
]