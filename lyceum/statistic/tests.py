import http

from django.test import TestCase
from django.urls import reverse
from parameterized import parameterized

from users.models import User
from rating.models import ItemRating
from catalog.models import Item, Category


class TestStatistic(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='admin', password="zxc")
        cls.category = Category.objects.create(slug='zxc', name='cat1')
        cls.bad_item = Item.objects.create(name='bad_item', category=cls.category, text="роскошно")
        cls.good_item = Item.objects.create(name='good_item', category=cls.category, text="роскошно")
        ItemRating.objects.create(user=cls.user, item=cls.bad_item, rating=2)
        ItemRating.objects.create(user=cls.user, item=cls.good_item, rating=5)

    @parameterized.expand([
        "statistic:best_worst",
        "statistic:rated_list",
        "statistic:item_rating_info"
    ])
    def test_endpoints(self, endpoint):
        self.client.force_login(self.user)
        response = self.client.get(reverse(endpoint))
        self.assertEqual(response.status_code, http.HTTPStatus.OK)

    def test_item_rating_info(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('statistic:item_rating_info'))
        for item in response.context['items']:
            self.assertEqual(item["rating_counts"], 1)
            if item["item"] == self.good_item:
                self.assertEqual(item["rating_middle"], 5.0)
            elif item["item"] == self.bad_item:
                self.assertEqual(item["rating_middle"], 2.0)

    def test_user_rating_info(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('statistic:best_worst'))
        self.assertIsInstance(response.context["best_item"], ItemRating)
        self.assertIsInstance(response.context["worst_item"], ItemRating)
        self.assertEqual(response.context["rating_middle"], 3.5)
        self.assertEqual(response.context["rating_counts"], 2)
