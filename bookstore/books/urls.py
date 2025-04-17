from django.urls import path
from . import views

urlpatterns = [
    path('', views.BookListView.as_view(), name='book_list'),
    path('<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),
    path('request-access/<int:book_id>/', views.request_access, name='request_access'),
    
    # Admin paths
    path('admin-panel/', views.AdminPanelView.as_view(), name='admin_panel'),
    path('admin-panel/users/', views.UserManagementView.as_view(), name='user_management'),
    path('admin-panel/requests/', views.AccessRequestsView.as_view(), name='access_requests'),
    path('admin-panel/handle-request/<int:request_id>/', views.handle_access_request, name='handle_request'),
    path('admin-panel/upload/', views.BookUploadView.as_view(), name='book_upload'),
]