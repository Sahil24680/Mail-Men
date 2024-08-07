from django.urls import path
from django.http import HttpResponse
from .import views




urlpatterns = [
    path('', views.get_emails, name='all_emails'),
    path('send_email/', views.send_email, name='send_email'),
    path('emaildelete/<int:email_id>/', views.delete_email, name='delete_email'),
    path('search/', views.search, name='search'),
    path('logout/', views.logout_, name='logout'),
    path('emaildetail/<int:id>/', views.clicked_email, name='email_detail'),
    path('profile/', views.Profile, name='profile'),
    path('newpfp/', views.newpfp, name='newpfp'),
    path('send_reply/<int:email_id>/', views.send_reply, name='send_reply'),
    path('archive_email/<int:email_id>/', views.archive, name='archive'),
    path('starred_email/<int:email_id>/', views.starred, name='starred'),
    path("archived",views.archived_emails,name ="archived"),
    path("starred",views.starred_emails,name ="starred"),
    path("graphs",views.Graph_data,name ="graphs"),
]
