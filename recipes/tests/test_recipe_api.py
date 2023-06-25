from unittest.mock import patch

from django.urls import reverse
from rest_framework import test

from recipes.tests.test_recipe_base import RecipeMixin


class RecipeAPIv2TestMixin(RecipeMixin):
    def api_url(self, reverse_result=None):
        url = reverse_result or reverse('recipes:recipes-api-list')
        response = self.client.get(url)
        return response

    def get_auth_data(self, username='user', password='pass'):
        userdata = {'username': username, 'password': password}
        user = self.make_author(
            username=username, password=password
        )
        response = self.client.post(
            reverse('recipes:token_obtain_pair'), data={**userdata}
        )
        return {
            'jwt_access': response.data.get('access'),
            'jwt_refresh': response.data.get('refresh'),
            'user': user,
        }

    def get_recipe_raw_data(self):
        return {
            'title': 'Recipe title',
            'description': 'Recipe description',
            'preparation_time': 1,
            'preparation_time_unit': 'Minutes',
            'servings': '1',
            'servings_unit': 'Portions',
            'preparation_steps': 'Recipe Preparation steps',
        }


class RecipeAPIv2Test(test.APITestCase, RecipeAPIv2TestMixin):
    def test_recipe_api_list_returns_status_code_200(self):
        url = reverse('recipes:recipes-api-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    @patch('recipes.views.api.RecipeAPIv2Pagination.page_size', new=7)
    def test_recipes_api_list_loads_correct_numbers_of_recipes(self):
        wanted_numbers_of_recipes = 7
        self.make_recipe_in_batch(qtd=wanted_numbers_of_recipes)

        response = self.api_url()
        qtd_of_loads_recipes = len(response.data.get('results'))

        self.assertEqual(qtd_of_loads_recipes, wanted_numbers_of_recipes)

    def test_recipes_api_list_do_not_show_not_published_recipes(self):
        recipes = self.make_recipe_in_batch(qtd=2)
        recipe_not_published = recipes[0]
        recipe_not_published.is_published = False
        recipe_not_published.save()

        response = self.api_url()
        self.assertEqual(len(response.data.get('results')), 1)

    def test_recipes_api_list_loads_recipes_by_category_id(self):
        # Creates categories
        category_wanted = self.make_category(name='wanted_category')
        category_not_wanted = self.make_category(name='not_wanted_category')
        recipes = self.make_recipe_in_batch(qtd=5)

        # Change all recipes to the wanted category
        for recipe in recipes:
            recipe.category = category_wanted
            recipe.save()

        # Change one recipes to the not wanted category
        # as a result, this recipe shold not show in the page
        recipes[0].category = category_not_wanted
        recipes[0].save()

        url = reverse('recipes:recipes-api-list') + \
            f'?category_id={category_wanted.id}'
        response = self.api_url(reverse_result=url)

        # We shold only see recipes from the wanted category
        self.assertEqual(len(response.data.get('results')), 4)

    def test_recipe_api_list_user_must_send_jwt_token_to_create_recipes(self):
        response = self.client.post(reverse('recipes:recipes-api-list'))
        self.assertEqual(response.status_code, 401)

    def teste_recipe_api_list_logged_user_can_create_a_recipe(self):
        recipe_raw_data = self.get_recipe_raw_data()
        auth_data = self.get_auth_data()
        access_token = auth_data.get('jwt_access')

        response = self.client.post(
            reverse('recipes:recipes-api-list'),
            data=recipe_raw_data,
            HTTP_AUTHORIZATION=f'Bearer {access_token}',
        )
        self.assertEqual(response.status_code, 201)

    def teste_recipe_api_list_logged_user_can_update_a_recipe(self):
        recipe = self.make_recipe()
        auth_data = self.get_auth_data()
        access_token = auth_data.get('jwt_access')
        author = auth_data.get('user')
        recipe.author = author
        recipe.save()

        response = self.client.patch(
            reverse('recipes:recipes-api-detail', args=(recipe.id,)),
            data={'title': 'new title'},
            HTTP_AUTHORIZATION=f'Bearer {access_token}',
        )

        self.assertEqual(
            response.data.get('title'), 'new title',
        )

    def teste_recipe_api_list_logged_user_cant_update_a_recipe_owned_by_another_user(self): # noqa
        recipe = self.make_recipe()
        auth_data = self.get_auth_data(username='test')

        # This user cannot update the recipe
        another_author = self.get_auth_data(username='another')
        access_token = another_author.get('jwt_access')

        # This is the actual owner of the recipe
        author = auth_data.get('user')
        recipe.author = author
        recipe.save()

        response = self.client.patch(
            reverse('recipes:recipes-api-detail', args=(recipe.id,)),
            HTTP_AUTHORIZATION=f'Bearer {access_token}',
        )

        # Another user cannot update the recipe, so the status code
        # is 403 Forbidden
        self.assertEqual(
            response.status_code, 403
        )
