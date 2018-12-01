from django.urls import path, include

urlpatterns = [
    path('kakaotalk/', include('main.urls')),
]

