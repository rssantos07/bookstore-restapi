import json

from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework.views import status


from product.factories import CategoryFactory
from product.models import Category


class CategoryViewSet(APITestCase):
    client = APIClient()

    def setUp(self):
        self.category = CategoryFactory(title="books")

    def test_get_all_category(self):
        response = self.client.get(
            reverse("category-list", kwargs={"version": "v1"}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        category_data = json.loads(response.content)

        self.assertEqual(category_data[0]["title"], self.category.title)

    def test_create_category(self):
        data = json.dumps({
            "title": "technology"
        })

        response = self.client.post(
            reverse("category-list", kwargs={"version": "v1"}),
            data=data,
            content_type="application/json",
        )


        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        created_category = Category.objects.get(title="technology")

        self.assertEqual(created_category.title, "technology")

    def test_delete_category(self):
        category_to_delete = CategoryFactory(title="category_to_delete")

        num_categories_before = Category.objects.count()

        response = self.client.delete(
            reverse("category-detail", kwargs={"version": "v1", "pk": category_to_delete.id}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        num_categories_after = Category.objects.count()
        self.assertEqual(num_categories_after, num_categories_before - 1)

        with self.assertRaises(Category.DoesNotExist):
            Category.objects.get(id=category_to_delete.id)