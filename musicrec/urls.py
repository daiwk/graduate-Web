from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'musicrec.views.home', name='home'),
    # url(r'^musicrec/', include('musicrec.foo.urls')),
    url(r'^musicrec/player.html', 'musicrec.views.player'),
    url(r'^musicrec/recommendation.html', 'musicrec.views.recommend'),
    url(r'^$', 'musicrec.views.index'),
    url(r'^polls/', include('musicrec.polls.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^music/(?P<path>.*)$', 'django.views.static.serve',{'document_root': '/home/daiwk/graduate/graduate-Web/music_django/djproj/trunk/music/'}),
    url(r'^imgs/(?P<path>.*)$', 'django.views.static.serve',{'document_root': '/home/daiwk/graduate/graduate-Web/music_django/djproj/trunk/imgs/'}),
    url(r'^css/(?P<path>.*)$', 'django.views.static.serve',{'document_root': '/home/daiwk/graduate/graduate-Web/music_django/djproj/trunk/css/'}),
    #url(r'^music/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT}),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/', 'musicrec.views.login_view'),
    url(r'^logout/', 'musicrec.views.logout_view'),
)

# Serve static files for admin, use this for debug usage only
# `python manage.py collectstatic` is preferred.
#from django.contrib.staticfiles.urls import staticfiles_urlpatterns
#urlpatterns += staticfiles_urlpatterns()
