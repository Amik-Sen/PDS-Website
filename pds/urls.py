from django.urls import path
from . import views

urlpatterns=[

    path('',views.home, name='home'),
    path('plan/',views.plan, name='plan'),
    path('visual/',views.visual, name='visual'),
    path('demand_rice/',views.demand_rice, name='demand_rice'),
    path('demand_wheat/',views.demand_wheat, name='demand_wheat'),
    path('demand_sugar/',views.demand_sugar, name='demand_sugar'),
]