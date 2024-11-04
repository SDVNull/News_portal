from django.urls import path
from .views import NewsList, NewsDetail, Publication_Create, Publication_Update, Publication_Delete

urlpatterns = [
   path('list/', NewsList.as_view(), name='list_news'),
   path('detail/<int:pk>', NewsDetail.as_view(), name='detail_news'),
   path('news/create/', Publication_Create.as_view(), name='publication_create'),
   path('news/<int:pk>/edit/', Publication_Update.as_view(), name='publication_update'),
   path('news/<int:pk>/delete/', Publication_Delete.as_view(), name='publication_delete'),
   path('article/create/', Publication_Create.as_view(), name='publication_create'),
   path('article/<int:pk>/edit/', Publication_Update.as_view(), name='publication_update'),
   path('article/<int:pk>/delete/', Publication_Delete.as_view(), name='publication_delete'),
]