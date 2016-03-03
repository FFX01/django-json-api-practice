from django.conf.urls import url
from . import views

urlpatterns = [
    url(
        r'^(?P<slug>[a-zA-Z0-9\-]+)/$',
        views.PageDetail.as_view(),
        name='page-detail'
    ),
    url(
        r'^$',
        views.PageList.as_view(),
        name='page-list'
    )
]
