from django.conf.urls import patterns, include, url
# from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'app.controller.home', name='home'),
    url(r'^suggestions/', 'app.controller.suggestions', name='suggestions'),
    url(r'^results/', 'app.controller.results', name='results'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),
)
