from django.urls import path
from home import views

urlpatterns = [
    # url for index page
    path('',views.index,name='index'),
    # url for about page
    path('about/',views.about,name='about'),
    # url for service page
    path('service/',views.service,name='service'),
    # url for registration of clients
    path('register/', views.register, name='register'),
    # url for login for customer and admin
    path('login/', views.login_view, name='login'),
    # url for login
    path('logout/', views.logout_view, name='logout'),
    # url for customer dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    # url for admin dashboard 
    path('admin-dashboard/',views.admin_dashboard,name='admin_dashboard'),
    # url for adding place 
    path('add-place/',views.add_place, name='add_place'),
    # url for bookin place 
    path('book/', views.book_place, name="book_place"),
    # url for adding places to the itinerary for customer
    path('add-to-itinerary/<int:place_id>/', views.add_to_itinerary, name='add_to_itinerary'),
    # url for viewing the view-itinerary
    path('view-itinerary/', views.view_itinerary, name='view_itinerary'),
    # url for confirm-booking
    path('confirm-booking/', views.confirm_booking, name='confirm_booking'),
    # url for payment-success
    path('payment-success/', views.payment_success, name='payment_success'),
    # url for admin-registration
    path("admin-register/", views.register_admin, name="admin_register"),
    # url for adding a package
    path("add-package/",views.add_package, name="add_package"),
    path("book-tour/", views.book_tour, name="book_tour"),
    path("booking-preview/<int:package_id>/", views.booking_preview, name="booking_preview"),
]
