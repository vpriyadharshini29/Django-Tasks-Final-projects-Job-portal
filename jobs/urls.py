from django.urls import path
from .views import (
    JobListView, JobDetailView, JobCreateView, JobUpdateView,
    JobDeleteView, ApplyJobView, signup_view, custom_logout
)

urlpatterns = [
    path("", JobListView.as_view(), name="job_list"),
    path("job/<int:pk>/", JobDetailView.as_view(), name="job_detail"),
    path("job/new/", JobCreateView.as_view(), name="job_create"),
    path("job/<int:pk>/edit/", JobUpdateView.as_view(), name="job_update"),
    path("job/<int:pk>/delete/", JobDeleteView.as_view(), name="job_delete"),
    path("job/<int:pk>/apply/", ApplyJobView.as_view(), name="apply_job"),  # ✅
    path("signup/", signup_view, name="signup"),
    path("logout/", custom_logout, name="logout"),
]
