from django.urls import path
from home import views

urlpatterns = [
    path('',views.index,name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admin-dashboard/',views.admin_dashboard,name='admin_dashboard'),
    path('add-place/',views.add_place, name='add_place'),
    path('book/', views.book_place, name="book_place"),
]
