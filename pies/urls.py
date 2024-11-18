from django.urls import path
from . import views

urlpatterns = [
   path('', views.pies),
   path('create_pie', views.create_pie),
   path('delete_pie', views.delete_pie),
   path('edit/<int:id>', views.edit_pie),
   path('edit/<int:id>/update', views.edit_pie_update),
   path('<int:id>', views.pie_vote),
   path('user_vote_pie', views.user_vote_pie),
   path('remove_user_vote_pie', views.remove_user_vote_pie),
]


