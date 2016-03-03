from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from .models import Page
from django.core import serializers


class PageList(View):

    def get(self, request):

        pages = Page.objects.all()

        pages_data = serializers.serialize('json', pages)

        return HttpResponse(
            content=pages_data,
            content_type='application/json'
        )

    def post(self, request):

        data = [obj for obj in serializers.deserialize('json', request.body)]

        if len(data) > 1:
            return HttpResponse(status=403)

        data[0].save()

        return HttpResponse(status=201)


class PageDetail(View):

    def get(self, request, slug):

        page = Page.objects.get(slug=slug)

        page_data = serializers.serialize('json', [page, ])

        return HttpResponse(
            content=page_data,
            content_type='application/json'
        )
