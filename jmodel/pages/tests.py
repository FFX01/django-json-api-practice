from django.test import TestCase, Client
from django.core import serializers
from .models import Page
import json


class PageListTest(TestCase):

    def setUp(self):

        self.client = Client()

        for n in range(10):
            new_page = Page(
                title='New Page %d' % n,
                slug='new-page-%d' % n
            )
            new_page.save()

    def test_can_retrieve_list_of_instances(self):

        response = self.client.get('/pages/')

        data = [obj for obj in serializers.deserialize('json', response.content.decode())]

        self.assertEqual(
            response.status_code,
            200,
            msg='Request did not return correct HTTP status code.'
        )

        self.assertEqual(
            len(data),
            10,
            msg='Request did not return correct number of instances.'
        )

        self.assertEqual(
            data[1].object.slug,
            'new-page-1',
            msg='Request did not return correct items.'
        )

    def test_can_create_new_instance(self):

        data = [
            {
                "model": "pages.page",
                "pk": None,
                "fields": {
                    "content": "",
                    "css": "",
                    "meta_description": "",
                    "meta_title": "",
                    "slug": "create-new-page",
                    "title": "Create New Page"
                }
            }
        ]

        json_data = json.dumps(data)

        response = self.client.post(
            path='/pages/',
            data=json_data,
            content_type='application/json'
        )

        self.assertEqual(
            response.status_code,
            201,
            msg='Request did not return correct HTTP response code.'
        )

        self.assertTrue(
            Page.objects.get(slug='create-new-page'),
            msg='Model instance could not be retrieved. Instance may not have been created.'
        )

    def test_cannot_POST_multiple_objects(self):

        data = [
            {
                "model": "pages.page",
                "pk": None,
                "fields": {
                    "content": "",
                    "css": "",
                    "meta_description": "",
                    "meta_title": "",
                    "slug": "create-new-page",
                    "title": "Create New Page"
                }
            },
            {
                "model": "pages.page",
                "pk": None,
                "fields": {
                    "content": "",
                    "css": "",
                    "meta_description": "",
                    "meta_title": "",
                    "slug": "create-new-page-1",
                    "title": "Create New Page 1"
                }
            }
        ]

        json_data = json.dumps(data)

        response = self.client.post(
            path='/pages/',
            data=json_data,
            content_type='application/json'
        )

        self.assertEqual(
            response.status_code,
            403,
            msg='Request did not return correct HTTP response code.'
        )

        self.assertRaises(
            excClass=Page.DoesNotExist,
            callableObj=Page.objects.get,
            slug='create-new-page-1'
        )


class PageDetailTest(TestCase):

    def setUp(self):

        self.client = Client()

        new_page = Page(
            title='Test Page 1',
            slug='test-page-1',
            meta_title='Test Meta Title',
            meta_description='Test Meta Description',
            css='.title{width:100%;}',
            content='Test Page Content'
        )
        new_page.save()

        wrong_page = Page(
            title='Wrong Page',
            slug='wrong-page',
            meta_title='Wrong Meta Title',
            meta_description='Wrong Meta Description',
            css='.wrong-title{width:100%;}',
            content='Wrong Page Content'
        )

        wrong_page.save()
        new_page.save()

        self.page = Page.objects.get(slug='test-page-1')
        self.wrong_page = Page.objects.get(slug='wrong-page')

    def test_can_retrieve_json(self):

        response = self.client.get('/pages/%s/' % self.page.slug)

        self.assertEqual(
            response.status_code,
            200,
            msg='Request did not return correct HTTP response code.'
        )
        self.assertEqual(
            response['Content-Type'],
            'application/json',
            msg='Request did not return correct Content-Type header.'
        )

    def test_can_retrieve_model_json(self):

        response = self.client.get('/pages/%s/' % self.page.slug)

        data = [obj for obj in serializers.deserialize('json', response.content.decode())]

        self.assertEqual(
            response.status_code,
            200,
            msg='Request did not return correct HTTP response code.'
        )

        self.assertEqual(
            len(data),
            1,
            msg="Request returned more than one model instance."
        )

        self.assertEqual(
            data[0].object.slug,
            self.page.slug,
            msg='Request did not return correct model instance.'
        )
