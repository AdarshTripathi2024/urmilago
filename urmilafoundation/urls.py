from django.urls import path
from . import views

urlpatterns = [ 
    path('', views.home, name='home'),
    path('about-urmila-foundation',views.about,name='about-us'),
    path('contact-us',views.contact,name='contact-us'),
    path('urmila-foundation-team',views.team,name='our-team'),
    path('director-urmila-foundation',views.director,name='our-director'),
    path('photo-gallery',views.gallery,name='photo-gallery'),
    path('e-gallery',views.e_gallery,name='e-gallery'),
    path('urmila-foundation-social-activities',views.social_activity,name='social-activities'),
    path('urmila-foundation-educational-acitvities',views.educational_activity,name='educational-activities'),
    path('donate-us',views.donate,name='donate-us'),
    path('become-a-volunteer',views.join_us,name='join-us'),
    path('facilities',views.facility,name='facility'),
    path('our-blogs',views.our_blogs,name='our-blogs'),
    path('blog/<int:id>/',views.blog,name='blog-detail'),
    path('faqs',views.faq,name='faqs'),
    path('subscribe-newsletter',views.subscribe,name='subscribe'),
    path('verify-otp',views.verify_otp,name="verify-otp"),
]
