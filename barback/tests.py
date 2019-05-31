from django.test import RequestFactory, TestCase
from django.contrib.auth.models import AnonymousUser, User
from django.conf import settings
from django.utils import timezone
from .models import Cocktail, User
from datetime import datetime, timedelta
from .forms import CocktailForm
from .views import ProfileView

# Create your tests here.
class CocktailTestCase(TestCase):
    def setUp(self):
        pub_time = timezone.now() - timedelta(days=1)
        Cocktail.objects.create(cocktail_name   ="cocktail",
                                pub_date        = pub_time,
                                cocktail_info   ="info",
                                cocktail_steps  ="steps",
                                virgin          = False,)
        Cocktail.objects.create(cocktail_name   ="virgin_cocktail",
                                pub_date        = pub_time,
                                cocktail_info   ="info",
                                cocktail_steps  ="steps",
                                virgin          = True,)

    def test_cocktail_is_virgin(self):
        virgin = Cocktail.objects.get(cocktail_name="virgin_cocktail")
        self.assertEqual(virgin.virgin, True)

    def test_cocktail_is_not_virgin(self):
        non_virgin = Cocktail.objects.get(cocktail_name="cocktail")
        self.assertEqual(non_virgin.virgin, False)

    def test_pub_date_is_correct(self):
        cocktail = Cocktail.objects.get(cocktail_name="cocktail")
        now = timezone.now()
        self.assertTrue(cocktail.pub_date < now)

    def test_string_fields_are_strings(self):
        cocktail = Cocktail.objects.get(cocktail_name="cocktail")
        self.assertTrue(isinstance(cocktail.cocktail_name, str))
        self.assertTrue(isinstance(cocktail.cocktail_info, str))
        self.assertTrue(isinstance(cocktail.cocktail_steps, str))

class CocktailFormTestCase(TestCase):
    def setUp(self):
        pub_time = timezone.now()
        cocktail = Cocktail.objects.create(cocktail_name   = "cocktail",
                                           pub_date        = pub_time,
                                           cocktail_info   = "info",
                                           cocktail_steps  = "steps",
                                           virgin          = False,)

    def test_init(self):
        cocktail = Cocktail.objects.get(cocktail_name="cocktail")
        CocktailForm({})

    def test_valid_data(self):
        form = CocktailForm({
            "cocktail_name" : "cocktail_name",
            "cocktail_type" : "WHISKEY",
            "cocktail_info" : "cocktail_info",
            "cocktail_steps": "cocktail_steps",
            "virgin"        : False,
        })
        self.assertTrue(form.is_valid())
        cocktail = form.save()
        self.assertEqual(cocktail.cocktail_name, "cocktail_name")
        self.assertEqual(cocktail.cocktail_type, "WHISKEY")
        self.assertEqual(cocktail.cocktail_info, "cocktail_info")
        self.assertEqual(cocktail.cocktail_steps, "cocktail_steps")
        self.assertEqual(cocktail.virgin, False)

    def test_blank_data(self):
        form = CocktailForm({})
        self.assertFalse(form.is_valid())

class UserTestCase(TestCase):
    def setUp(self):
        # self.factory = RequestFactory()
        pass

    def test_user_fields(self):
        User.objects.create()
        user = User.objects.create()
        self.assertEqual(user.username, "test")

    # def test_profile(self):
    #     request = self.factory.get('profile/')
    #     request.user = self.user
    #     response = ProfileView(request)
    #     response = ProfileView.as_view()(request)
    #     self.assertEqual(response.status_code, 200)
