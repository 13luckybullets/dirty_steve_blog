from django.conf.urls import url
from django.contrib import admin
from coding_blog import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.articles, name="home"),
    url(r'^post/(?P<pk>[0-9]+)/$', views.get_post, name='get_post'),
    url(r'^sign_up/$', views.sign_up, name='sign_up'),
    url(r'^sign_in/$', auth_views.login, {'template_name': 'sign_in.html'}, name='sign_in'),
    url(r'^sign_out/$', auth_views.logout, {'next_page': 'home'}, name='sign_out'),
    url(r'^add_post/$', views.add_post, name='add_post'),
    url(r'^add_like/post(?P<post>[0-9]+)_user(?P<user>[0-9]+)/$', views.add_like, name="add_like"),
    url(r'^edit_post(?P<pk>[0-9]+)/$', views.edit_post, name='edit_post'),
    url(r'^add_comment/post(?P<pk>[0-9]+)/$', views.add_comment, name="add_comment"),
    url(r'^profile(?P<pk>[0-9]+)/$', views.profile, name='profile'),
    url(r'^edit_profile(?P<pk>[0-9]+)/$', views.edit_profile, name='edit_profile')
]
