from django.conf.urls import patterns, include, url
import webapp.views
import apps.authentication.views
# Uncomment the next two lines to enable the admin:

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'WebApp.views.home', name='home'),
    # url(r'^WebApp/', include('webapp.foo.urls')),
    
    # ############################ #
    # ########  HTML URLS ######## #
    # ############################ #
    url(r'^$',webapp.views.BaseView),
    url(r'^signup$',apps.authentication.views.SignUpView),
    url(r'^signin$',apps.authentication.views.SignInView),
    url(r'^logout$',apps.authentication.views.LogOutView),
    url(r'^passwd_recover$',apps.authentication.views.PasswordRecoverView),
    url(r'^passwd_recover/(?P<username>[a-zA-Z0-9_-]{3,20}$)$',apps.authentication.views.PasswordRecoverFormView),
    
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    
    # ############################ #
    # ######### API URLS ######### #
    # ############################ #
    url(r'^api/signup$',apps.authentication.views.SignUpView),
    url(r'^api/signin$',apps.authentication.views.SignInView),
)
