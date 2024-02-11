from django.urls import path
from . import views


urlpatterns = [

    path('admin_panel/', views.admin_panel, name="admin_panel"),
    path('admin_users/', views.AdminUsersView.as_view(), name="admin_users"),
    path('activate_users/', views.activate_users, name="activate_users"),
    path('inactivate_users/', views.inactivate_users, name="inactivate_users"),
    path('delete_users/', views.delete_users, name="delete_users"),
    path('admin_review/', views.AdminReviewView.as_view(), name="admin_review"),
    path('admin_charts/', views.AdminChartsView.as_view(), name="admin_charts"),
    path('admin_archive/', views.AdminArchiveView.as_view(), name="admin_archive"),
    path('lesson_details/<booking_id>', views.admin_lesson_details, name="lesson_details"),
    path('admin_finalize/', views.AdminFinalizeView.as_view(), name="admin_finalize")
]
