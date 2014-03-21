from django.conf.urls import patterns, include, url
from exchange import views as exchange_views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'rch.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^exchange/deposit$', exchange_views.DepositView.as_view(), name='deposit'),

)
