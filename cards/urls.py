from django.contrib import admin
from django.urls import path
from cards import views

urlpatterns = [
    path('catalog/', views.CatalogView.as_view(), name='catalog'),
    path('<int:pk>/detail/', views.CardDetailView.as_view(), name='detail_card_by_id'),
    path('tags/<int:tag_id>/', views.get_cards_by_tag, name='cards_by_tag'),
    path('add_card/', views.AddCardCreateView.as_view(), name='add_card'),
]
