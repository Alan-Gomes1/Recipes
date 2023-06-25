from django.contrib.auth.models import User
from django.test import TestCase

from recipes.models import Category, Recipe


class RecipeMixin:
    def make_category(self, name='Category'):
        """
        Creates a new Category object with the specified name and returns it.

        :param name: (str) the name of the category,
        defaults to 'Category' if not provided
        :return: (Category) the newly created Category object
        """

        return Category.objects.create(name=name)

    def make_author(
        self,
        first_name='user',
        last_name='name',
        username='username',
        password='123456',
        email='username@email.com',
    ):
        """
        Creates a new user with the given first name, last name, username,
        password, and email.

        :return: A new User object with the specified parameters.
        """

        return User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
            email=email,
        )

    def make_recipe(
        self,
        category_data=None,
        author_data=None,
        title='Recipe title',
        description='Recipe description',
        slug='recipe-slug',
        preparation_time=10,
        preparation_time_unit='Minutes',
        servings=5,
        servings_unit='Portions',
        preparation_steps='Recipe Preparation steps',
        preparation_steps_is_html=False,
        is_published=True,
        cover='recipes/covers/2023/03/24/Pão_de_hambúrguer_-_Guia_da_Cozinha_rzvdr5d.jpeg', # noqa
    ):
        """
            Creates and returns a new Recipe object with the given parameters.
        """

        if category_data is None:
            category_data = {}

        if author_data is None:
            author_data = {}

        return Recipe.objects.create(
            category=self.make_category(**category_data),
            author=self.make_author(**author_data),
            title=title,
            description=description,
            slug=slug,
            preparation_time=preparation_time,
            preparation_time_unit=preparation_time_unit,
            servings=servings,
            servings_unit=servings_unit,
            preparation_steps=preparation_steps,
            preparation_steps_is_html=preparation_steps_is_html,
            is_published=is_published,
            cover=cover,
        )

    def make_recipe_in_batch(self, qtd=10):
        """
            Creates a batch of recipe objects, given a quantity.

            :param qtd: An integer that specifies the number of recipe objects
            to create. Default is 10.
            :type qtd: int

            :return: A list of recipe objects.
            :rtype: list
        """

        recipes = []
        for i in range(qtd):
            kwargs = {
                'title': f'Recipe title {i}',
                'slug': f'r{i}',
                'author_data': {'username': f'u{i}'}
                }
            recipe = self.make_recipe(**kwargs)
            recipes.append(recipe)
        return recipes


class RecipeTestBase(TestCase, RecipeMixin):
    def setUp(self) -> None:
        return super().setUp()
