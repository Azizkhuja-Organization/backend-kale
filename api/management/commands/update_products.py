from django.core.management.base import BaseCommand, CommandError
from polls.models import Question as Poll


import base64
import datetime

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile

from api.auth.send_sms_func import sent_sms_base
from common.product.models import Product, Category, SubCategory
from common.users.models import Code
from kale.utils.one_s_get_products import get_products, get_product_photo


User = get_user_model()


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def add_arguments(self, parser):
        parser.add_argument("poll_ids", nargs="+", type=int)

    def handle(self, *args, **options):
        print(datetime.datetime.now(), "START")
        products = get_products()
        newProducts = []
        updateProducts = []
        for product in products.get("Товары"):
            category_name = product.get("Категория")
            quantity = product.get("Остаток")
            code = product.get("Код")
            price = product.get("Цена")
            title = product.get("Наименование")
            unit = product.get("ЕдиницаИзмерения")
            brand = product.get("ТорговаяМарка")
            size = product.get("Размеры")
            description = product.get("Описание")
            manufacturer = product.get("Производитель")
            if category_name and code and price > 0 and quantity > 0 and title:
                category = SubCategory.objects.filter(title_ru=category_name).first()
                if category is None:
                    continue
                pr = Product.objects.filter(code=code).first()

                photo_content = None

                if pr and pr.code == code: # and pr.quantity < quantity:
                    if pr.photo is None:
                        photo = get_product_photo(code)
                        if photo:
                            photo_data = photo.split(";base64,")[1]
                            photo_content = ContentFile(base64.b64decode(photo_data), name=f"{code}_photo.png")
                    updateProducts.append(Product(
                        id=pr.id,
                        subcategory=category,
                        # title=title,
                        title_ru=title,
                        description_ru=description,
                        price=price,
                        # material_ru=material,
                        unit=unit,
                        brand=brand,
                        size=size,
                        manufacturer_ru=manufacturer,
                        quantity=quantity,
                        photo=photo_content
                    ))
                elif pr is None:
                    photo = get_product_photo(code)
                    if photo:
                        photo_data = photo.split(";base64,")[1]
                        photo_content = ContentFile(base64.b64decode(photo_data), name=f"{code}_photo.png")
                    newProducts.append(Product(
                        subcategory=category,
                        code=code,
                        # title=title,
                        title_ru=title,
                        description_ru=description,
                        price=price,
                        # material_ru=material,
                        unit=unit,
                        brand=brand,
                        size=size,
                        manufacturer_ru=manufacturer,
                        quantity=quantity,
                        photo=photo_content
                    ))
        if newProducts:
            Product.objects.bulk_create(newProducts)
        if updateProducts:
            Product.objects.bulk_update(updateProducts,
                                        fields=['subcategory', 'title_ru', 'description_ru', 'price', 'unit', 'brand',
                                                'size',
                                                'manufacturer_ru', 'quantity'])

        print(datetime.datetime.now(), "END")
        return