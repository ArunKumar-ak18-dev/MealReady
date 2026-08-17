from django.urls import path
from . import views

urlpatterns = [
    path('',views.welcome,name='welcome'),
    path('open_signup',views.open_signup, name='open_signup'),
     path('open_signin',views.open_signin, name='open_signin'),
     path('signup',views.signup, name='signup'),
     path('signin',views.signin, name='signin'),
     path('open_add_restaurent',views.open_add_restaurent,name="open_add_restaurent"),
     path('add_restaurent', views.add_restaurent, name='add_restaurent'),
     path('show_restaurents', views.show_restaurents, name='show_restaurents'),
     path('open_add_items/<int:restaurant_id>', views.open_add_items, name='open_add_items'), 
     path("add_items/<int:restaurant_id>/", views.add_items, name="add_items"),
     path("show_res_cus/<str:username>/",views.show_res_cus,name="show_res_cus"),  
     path('open_update_restaurant/<int:restaurant_id>/',views.open_update_restaurant, name="open_update_restaurant"),
     path('update_restaurant/<int:restaurant_id>/', views.update_restaurant, name="update_restaurant"),
     path('delete_restaurant/<int:restaurant_id>/', views.delete_restaurant, name="delete_restaurant"),
     path('view_menu/<int:restaurant_id>/<str:username>/',views.view_menu,name="view_menu"),
     path('add_to_cart/<int:item_id>/<str:username>', views.add_to_cart, name='add_to_cart'),
     path('view_cart/<str:username>', views.view_cart, name='view_cart'),
     path('orders/<str:username>/', views.orders, name='orders'),
]


