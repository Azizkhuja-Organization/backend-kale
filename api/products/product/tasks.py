from celery import shared_task

from common.product.models import Product, Category, SubCategory
from kale.utils.one_s_get_products import get_products


@shared_task(name='updateProducts')
def updateProducts():
    for i in Product.objects.all():
        i.delete()

    products = get_products()
    newProducts = []
    updateProducts = []
    for product in products.get("Товары"):
        category_name = product.get("Категория")
        code = product.get("Код")
        price = product.get("Цена")
        title = product.get("Наименование")
        if not code or not price or not category_name or not title:
            continue
        unit = product.get("ЕдиницаИзмерения")
        brand = product.get("ТорговаяМарка")
        size = product.get("Размеры")
        description = product.get("Описание")
        manufacturer = product.get("Производитель")
        quantity = product.get("Остаток")
        category = SubCategory.objects.filter(title_ru=category_name).first()
        if category is None:
            continue

        pr = Product.objects.filter(code=code).first()
        if pr and pr.code == code:
            updateProducts.append(Product(
                id=pr.id,
                category=category,
                # title=title,
                title_ru=title,
                description_ru=description,
                price=price,
                # material_ru=material,
                unit=unit,
                brand=brand,
                size=size,
                manufacturer_ru=manufacturer,
                quantity=quantity
            ))
        else:
            newProducts.append(Product(
                category=category,
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
                quantity=quantity
            ))
    if newProducts:
        Product.objects.bulk_create(newProducts)
    if updateProducts:
        Product.objects.bulk_update(updateProducts,
                                    fields=['category', 'title_ru', 'description_ru', 'price', 'unit', 'brand', 'size',
                                            'manufacturer_ru', 'quantity'])
    return


categories = [
    {
        "title": "Унитаз",
        "subcategories": ["Унитаз подвесной", "Унитаз смарт", "Унитаз стоячий", "Биде подвесной", "Биде стоячий"]
    },
    {
        "title": "Смеситель",
        "subcategories": ['Смеситель встроенный', 'Смеситель для биде', 'Смеситель для ванны', 'Смеситель для раковины',
                          'Смеситель кухонный', 'Смеситель для душа', 'Смеситель от пола']
    },
    {
        "title": "Раковина",
        "subcategories": ["Раковина"]
    },
    {
        "title": "Мебель для ванной комнаты",
        "subcategories": ["Пенал", "Шкаф"]
    },
    {
        "title": "Кафель",
        "subcategories": ["Декор", "Кафель половой", "Кафель стеновой"]
    },
    {
        "title": "Калесинтерфлекс",
        "subcategories": ["Калесинтерфлекс"]
    },
    {
        "title": "Инсталляции",
        "subcategories": ["Инсталляции", "Кнопка"]
    },
    {
        "title": "Душевая система",
        "subcategories": ["Душ система", "Лейка со стойкойй", "Лейка", "Шланг"]
    },
    {
        "title": "Ванна",
        "subcategories": ["Ванна", "Ванна отдельностоящая", "Джакузи", "Душевая кабина" "Поддоны и перегородки"]
    },
    {
        "title": "Аксессуары и прочие",
        "subcategories": ["Аксессуары", "Гофра", "Сифон"]
    },
    {
        "title": "Полотенцесущитель",
        "subcategories": ["Полотенцесущитель"]
    },
    {
        "title": "Трапы",
        "subcategories": ["Трапы"]
    }
]


def createCategories():
    subcategories = []
    for i in categories:
        category, created = Category.objects.get_or_create(title_ru=i.get('title'))
        if created:
            for j in i.get('subcategories'):
                subcategories.append(SubCategory(category=category, title_ru=j))
    if subcategories:
        SubCategory.objects.bulk_create(subcategories)
