from django.urls import path
from . import views

app_name = "rooms"

urlpatterns = [path("list/", views.RoomsView.as_view()),
               path("search/", views.room_search),
               path("<int:pk>", views.SeeRoomView.as_view()),]
