"""
URL configuration for NetWork project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import bot, auth
from .views_class import HomeView, AddBoardView, MyBoardsView, BoardDetailView, BoardDeleteView, ColumnCreateView, \
    DeleteColumnView, AddTaskView, DeleteTaskView, EditTaskView, AddCollaboratorView, DeleteCollaboratorView, \
    ViewThemesView, AddThemeView, EditThemeView, EditBoardView, EditColumnView, TaskConsumer

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/',
         SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/',
         SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include('core.urls')),

    path('', HomeView.as_view(), name='home'),
    path('my_boards/', MyBoardsView.as_view(), name='my_boards'),
    path('add_board/', AddBoardView.as_view(), name='add_board'),
    path('board/<int:pk>/', BoardDetailView.as_view(), name='board_detail'),
    path('delete_board/<int:pk>/', BoardDeleteView.as_view(), name='delete_board'),
    path('add_column/<int:id>/', ColumnCreateView.as_view(), name='add_column'),
    path('delete_column/<int:pk>/', DeleteColumnView.as_view(), name='delete_column'),
    path('add_task/<int:board_id>/<int:column_id>/', AddTaskView.as_view(), name='add_task'),
    path('delete_task/<int:pk>/', DeleteTaskView.as_view(), name='delete_task'),
    path('edit_task/<int:pk>/', EditTaskView.as_view(), name='edit_task'),
    path('add_collaborator/<int:board_id>/', AddCollaboratorView.as_view(), name='add_collaborator'),
    path('delete_collaborator/<int:board_id>/<int:collaborator_id>/', DeleteCollaboratorView.as_view(),
         name='delete_collaborator'),
    path('view_themes/', ViewThemesView.as_view(), name='view_themes'),
    path('add_theme/', AddThemeView.as_view(), name='add_theme'),
    path('edit_theme/<int:pk>/', EditThemeView.as_view(), name='edit_theme'),
    path('edit_board/<int:pk>/', EditBoardView.as_view(), name='edit_board'),
    path('edit_column/<int:pk>/', EditColumnView.as_view(), name='edit_column'),

    path('sign_up/', auth.sign_up, name='sign_up'),
    path('login/', auth.user_login, name='login'),
    path('logout/', auth.user_logout, name='logout'),
    path('edit/', auth.edit_profile, name='edit_profile'),

    path('subscribe_on_events/', bot.subscribe_on_events, name='subscribe_on_events'),
    path('unsubscribe_from_events/', bot.unsubscribe_from_events, name='unsubscribe_from_events'),

    path('accounts/', include('allauth.urls')),

]

websocket_urlpatterns = [
    path('ws/tasks/', TaskConsumer.as_asgi())
]

urlpatterns += [
    path('ws/', include(websocket_urlpatterns)),
]
