from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'booksdb.views.home', name='home'),
    # url(r'^booksdb/', include('booksdb.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^mybooks/$', 'mybooks.views.index'),
    url(r'^mybooks/(?P<poll_id>\d+)/$', 'mybooks.views.detail'),
    url(r'^admin/', include(admin.site.urls)),
)
