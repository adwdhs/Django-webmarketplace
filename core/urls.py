from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginForm

urlpatterns = [
    path('', views.browse, name='items'),
    path('message/<str:pk>', views.message, name='message'),
    path('inbox', views.inbox, name='inbox'),
    path('new/<str:item_pk>', views.newConversation, name='new'),
    path('contacts/', views.contacts, name='contacts'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('new/', views.newItem, name='new'),
    path('details/<str:pk>', views.detail, name='details'),
    path('delete/<str:pk>', views.deleteItem, name='delete'),
    path('edit/<str:pk>', views.editItem, name='edit'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('sighup/', views.sighup, name='sighup'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html', authentication_form=LoginForm), name='login')



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


