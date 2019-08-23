from django.urls import include, path

urlpatterns = [
    path('search/', include('search.urls')),
    path('company/', include('company.urls')),
]
