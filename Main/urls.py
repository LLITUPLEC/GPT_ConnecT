from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views

urlpatterns = [
    path('', views.index, name='home'),
    path('kmo', views.kmo, name='kmo'),
    path('about', views.about, name='about'),
    path('zadeploil', views.zadeploil, name='zadeploil'),
    path('bs', views.bs, name='bs'),
    path('create_kmo_det/<int:kmo_id>/<int:kmo_det_department>', views.create_kmo_det, name='create_kmo_det'),
    # path('check_create_kmo', views.check_create_kmo, name='check_create_kmo'),
    path('register/', user_views.register, name='register'),
    path('profile/', user_views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('delete/<int:kmo_id>', views.delete, name='delete'),
    path('delete_kmo_det/<int:kmodet_id>', views.delete_kmo_det, name='delete_kmo_det'),
    path('edit_kmo/<int:kmo_id>', views.edit_kmo, name='edit_kmo'),
    path('edit_kmo_det/<int:kmodet_id>', views.edit_kmo_det, name='edit_kmo_det'),
    path('view_kmo/<int:kmo_id>', views.view_kmo, name='view_kmo'),
    path('view_kmo_det/<int:kmodet_id>', views.view_kmo_det, name='view_kmo_det'),
    path('kmo_pdf/<int:kmo_id>', views.kmo_pdf, name='kmo_pdf'),
    path('delete_members/<int:form_h_id>', views.delete_members, name='delete_members'),
    path('done_kmo_det/<int:kmodet_id>', views.done_kmo_det, name='done_kmo_det'),
    path('view_kmodet_by_qr/<str:type_obj>/<int:id_obj>', views.view_kmodet_by_qr, name='view_kmodet_by_qr'),
    path('qr/', views.index_qr, name='qr-generator'),
    path('approv_kmo/<int:kmo_id>', views.approv_kmo, name='approv_kmo'),
    path('export_kmodet_xls/<int:kmo_id>', views.export_kmodet_xls, name='export_kmodet_xls'),

]

