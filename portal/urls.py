from django.urls import path
from .views import NewsList, NewsDetail, PublicationCreate, PublicationUpdate, PublicationDelete, subscriptions

app_name = 'portal'

urlpatterns = [
   path('list/', NewsList.as_view(), name='list_news'),
   path('detail/<int:pk>', NewsDetail.as_view(), name='detail_news'),
   path('news/create/', PublicationCreate.as_view(), name='publication_create'),
   path('news/<int:pk>/edit/', PublicationUpdate.as_view(), name='publication_update'),
   path('news/<int:pk>/delete/', PublicationDelete.as_view(), name='publication_delete'),
   path('article/create/', PublicationCreate.as_view(), name='publication_create'),
   path('article/<int:pk>/edit/', PublicationUpdate.as_view(), name='publication_update'),
   path('article/<int:pk>/delete/', PublicationDelete.as_view(), name='publication_delete'),
   path('subscriptions/', subscriptions, name='subscriptions'),
]