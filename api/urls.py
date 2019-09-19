from django.conf.urls import url
from api import views

urlpatterns = [
    url(r'^(?P<version>[v1|v2]+)/user$', views.UserView.as_view(), name= 'user'),
    url(r'^(?P<version>[v1|v2]+)/parser$', views.ParserView.as_view(), name= 'parser'),
    url(r'^(?P<version>[v1|v2]+)/roles$', views.RolesView.as_view(), name= 'roles'),
    url(r'^(?P<version>[v1|v2]+)/userinfo$', views.UserInfoView.as_view(), name= 'roles'),
    url(r'^(?P<version>[v1|v2]+)/group/(?P<pk>\d+)$', views.GroupView.as_view(), name= 'group'),
    url(r'^(?P<version>[v1|v2]+)/usergroup$', views.UserGroupView.as_view(), name= 'usergroup'),
]