from django.urls import path
from boat_manager import views

urlpatterns = [
    path('pier_create/', views.create_pier, name='pier_create'),
    path('pier_edit/<int:pier_id>',views.pier_edit, name='pier_edit'),
    path('pier_delete/<int:pier_id>', views.pier_delete, name='pier_delete'),
    path('piers/', views.pier_list, name='piers'),
    path('boat_create/', views.create_boat, name='boat_create'),
    path('boats/', views.boat_list, name='boats'),
    path('boat_edit/<int:boat_id>', views.boat_edit, name='boat_edit'),
    path('boat_delete/<int:boat_id>', views.boat_delete, name='boat_delete'),
    path('boat_detail/<int:boat_id>', views.boat_detail, name='boat_detail'),
    path('register/', views.register, name='register'),
    path('', views.home, name='home'),
    path('login_page/', views.login_user, name='login_page'),
    path('logout_page/', views.logout_user, name='logut_page'),
    path('booking_details/<int:boat_id>', views.rent, name='booking_details'),
    path('booking_confirmation/<int:boat_id>', views.booking_details, name='booking_confirmation'),
    path('bookings_list/', views.bookings_list, name='bookings_list'),
    path('customer_bookins_list/', views.customer_booking_list, name='customer_bookins_list'),
    path('booking_edit/<int:booking_id>', views.booking_edit, name='booking_edit'),
    path('booking_delete/<int:booking_id>', views.booking_cancel, name='booking_cancel',),
    path('booking_status/<int:booking_id>', views.booking_status, name='booking_status'),
    path('customer_detail/<int:user_id>', views.customer_detail, name='customer_detail'),
    path('customer_list', views.customer_list, name='customer_list'),
    path('export/', views.export_bookings, name='export_bookings'),
]