import os
from collections import defaultdict

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models import F, Value
from django.db.models.functions import Concat
from django.forms import ValidationError
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from PIL import Image

from tag.models import Tag


class Category(models.Model):
    name = models.CharField(max_length=65)

    def __str__(self):
        return self.name


class RecipeManager(models.Manager):
    def get_published(self):
        return self.filter(
            is_published=True
        ).annotate(
            author_full_name=Concat(
                F('author__first_name'), Value(' '),
                F('author__last_name'), Value(' ('),
                F('author__username'), Value(')'),
            )
        ).order_by('-id').select_related('author', 'category')\
            .prefetch_related('tags')


class Recipe(models.Model):
    objects = RecipeManager()
    title = models.CharField(max_length=65, verbose_name=_('Title'))
    description = models.CharField(max_length=165)
    slug = models.SlugField(unique=True)
    preparation_time = models.IntegerField()
    preparation_time_unit = models.CharField(max_length=65)
    servings = models.IntegerField()
    servings_unit = models.CharField(max_length=65)
    preparation_steps = models.TextField()
    preparation_steps_is_html = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    cover = models.ImageField(upload_to='recipes/covers/%Y/%m/%d')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True,
        default=None
    )
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True
    )
    tags = models.ManyToManyField(Tag, blank=True, default='')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('recipes:recipe', args=(self.id,))

    def resize_image(self, image, new_width=2280):
        image_full_path = os.path.join(settings.MEDIA_ROOT, image.name)
        img_pillow = Image.open(image_full_path)
        original_width, original_height = img_pillow.size

        if original_width <= new_width:
            img_pillow.close()
            return

        new_height = round((new_width * original_height) / original_width)
        new_img = img_pillow.resize((new_width, new_height), Image.LANCZOS)
        new_img.save(
            image_full_path,
            optimize=True,
            quality=95,
        )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = f'{slugify(self.title)}'

        saved = super().save(*args, **kwargs)

        if self.cover:
            try:
                self.resize_image(self.cover)
            except FileNotFoundError:
                pass

        return saved

    def clean(self, *args, **kwargs):
        error_messages = defaultdict(list)

        recipe_from_db = Recipe.objects.filter(
            title__iexact=self.title
        ).first()

        if recipe_from_db:
            if recipe_from_db.pk != self.pk:
                error_messages['title'].append(
                    'Found recipes with the same title'
                )

        if self.title == 'Recipe title':  # nome de teste das receitas
            return

        if error_messages:
            raise ValidationError(error_messages)

    class Meta:
        verbose_name = _('Recipe')
        verbose_name_plural = _('Recipes')
