from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('',views.home, name="" ),

    path('register', views.register, name="register"),

    path('my-login', views.my_login, name="my-login"),

    path('user-logout', views.user_logout, name="user-logout"),

    path('dashboard',views.dashboard, name="dashboard"),

    # CRUD

    path('dashboard', views.dashboard, name="dashboard"),

    path('create-record', views.create_record, name='create-record'),

    path('update-record/<int:pk>',views.update_record, name='update-record' ),

    path('record/<int:pk>', views.singular_record, name="record"),

    path('datete-record/<int:pk>', views.delete_record,name="delete-record"),
    
    path('search', views.search_records, name='search-records'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
