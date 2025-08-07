from django.urls import path

from mailings import views
from mailings.apps import MailingsConfig

app_name = MailingsConfig.name

urlpatterns = [
    path('home/', views.HomeTemplateView.as_view(), name='home'),
    path('recipients/', views.RecipientListView.as_view(), name='recipient_list'),
    path('recipients/add/', views.RecipientCreateView.as_view(), name='recipient_create'),
    path('recipients/<int:pk>/', views.RecipientDetailView.as_view(), name='recipient_detail'),
    path('recipients/<int:pk>/update/', views.RecipientUpdateView.as_view(), name='recipient_update'),
    path('recipients/<int:pk>/delete/', views.RecipientDeleteView.as_view(), name='recipient_delete'),
    path('messages/', views.MessageListView.as_view(), name='message_list'),
    path('messages/add/', views.MessageCreateView.as_view(), name='message_create'),
    path('messages/<int:pk>/', views.MessageDetailView.as_view(), name='message_detail'),
    path('messages/<int:pk>/update/', views.MessageUpdateView.as_view(), name='message_update'),
    path('messages/<int:pk>/delete/', views.MessageDeleteView.as_view(), name='message_delete'),
    path('mailings/', views.MailingListView.as_view(), name='mailing_list'),
    path('mailings/add/', views.MailingCreateView.as_view(), name='mailing_create'),
    path('mailings/<int:pk>/', views.MailingDetailView.as_view(), name='mailing_detail'),
    path('mailings/<int:pk>/update/', views.MailingUpdateView.as_view(), name='mailing_update'),
    path('mailings/<int:pk>/delete/', views.MailingDeleteView.as_view(), name='mailing_delete'),
]
