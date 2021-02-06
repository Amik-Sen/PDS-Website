from django.urls import path
from . import views

urlpatterns=[

    path('',views.home, name='home'),
    path('plan/',views.plan, name='plan'),
    path('visual/',views.visual, name='visual'),
]