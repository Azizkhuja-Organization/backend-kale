import base64

from django.core.files.base import ContentFile
from django.db.models import Q, Exists, OuterRef, F
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, ListAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from api.paginator import CustomPagination
from api.permissions import IsAdmin
from api.products.images.serializers import ProductImageCreateSerializer
from api.products.product.serializers import ProductCreateSerializer, ProductListSerializer, ProductDetailSerializer, \
    ProductUpdateSerializer
from common.order.models import Wishlist, Comparison, CartProduct
from common.product.models import Product, ProductImage, SubCategory
from kale.utils.one_s_get_products import get_product_photo, get_products


class ProductCreateAPIView(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductCreateSerializer
    permission_classes = [IsAdmin]

    def create(self, request, *args, **kwargs):
        photos = None
        if 'photos' in request.data:
            photos = request.data.pop('photos')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()
        if photos:
            obj = []
            for photo in photos:
                serial = ProductImageCreateSerializer(data={
                    "product": product.id,
                    "photo": photo
                })
                serial.is_valid(raise_exception=True)
                obj.append(ProductImage(product=product, photo=serial.validated_data.get('photo')))
            if obj:
                ProductImage.objects.bulk_create(obj)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductUpdatesAPIView(APIView):
    def get(self):
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

                if pr and pr.code == code:  # and pr.quantity < quantity:
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
        return Response(status=status.HTTP_200_OK)


class ProductListAPIView(ListAPIView):
    queryset = Product.objects.select_related('subcategory', 'subcategory__category').all()
    serializer_class = ProductListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['subcategory', 'unit', 'status', 'brand', 'manufacturer', 'cornerStatus', 'isTop']

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            wishlist, created = Wishlist.objects.get_or_create(user_id=self.request.user.id)
            comparison, created2 = Comparison.objects.get_or_create(user_id=self.request.user.id)

            queryset = queryset.annotate(
                isLiked=Exists(wishlist.products.all().filter(id__in=OuterRef('pk')))).annotate(
                isCompared=Exists(comparison.products.all().filter(id__in=OuterRef('pk')))).annotate(
                isCart=Exists(CartProduct.objects.filter(product_id=OuterRef('pk'),
                                                         cart__user_id=self.request.user.id))).annotate(
                cartProductQuantity=F('cartProduct__quantity'))

        hasLiked = self.request.query_params.get('hasLiked')
        if hasLiked and self.request.user.is_authenticated:
            queryset = queryset.filter(isLiked=True)

        hasCompared = self.request.query_params.get('hasCompared')
        if hasCompared and self.request.user.is_authenticated:
            queryset = queryset.filter(isCompared=True)

        others = self.request.query_params.get('others')
        guid = self.request.query_params.get('guid')
        product = Product.objects.filter(guid=guid).first()
        if others and product:
            try:
                queryset = queryset.filter(subcategory=product.subcategory).exclude(guid=guid)
            except:
                pass

        has3D = self.request.query_params.get('has3D')
        if has3D:
            queryset = queryset.filter(file3D__isnull=False)

        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(subcategory__category=category)

        min = self.request.query_params.get('min')
        max = self.request.query_params.get('max')
        if min and max:
            queryset = queryset.filter(price__gte=min, price__lte=max)

        elif min:
            queryset = queryset.filter(price__gte=min)

        elif max:
            queryset = queryset.filter(price__lte=max)
        q = self.request.query_params.get('q')
        if q:
            queryset = queryset.filter(Q(title__icontains=q))
        p = self.request.query_params.get('p')
        if p:
            self.pagination_class = CustomPagination
        return queryset


class ProductDetailAPIView(RetrieveAPIView):
    queryset = Product.objects.select_related('subcategory').all()
    serializer_class = ProductDetailSerializer
    lookup_field = 'guid'

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            wishlist, created = Wishlist.objects.get_or_create(user_id=self.request.user.id)
            queryset = queryset.annotate(isLiked=Exists(wishlist.products.all().filter(id__in=OuterRef('pk'))))

            comparison, created2 = Comparison.objects.get_or_create(user_id=self.request.user.id)
            queryset = queryset.annotate(isCompared=Exists(comparison.products.all().filter(id__in=OuterRef('pk'))))

            queryset = queryset.annotate(isCart=Exists(
                CartProduct.objects.filter(product_id=OuterRef('pk'), cart__user_id=self.request.user.id)))
        return queryset


class ProductUpdateAPIView(UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductUpdateSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'guid'

    def update(self, request, *args, **kwargs):
        photos = request.data.pop('photos')
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if photos:
            obj = []
            for photo in photos:
                serial = ProductImageCreateSerializer(data={
                    "product": instance.id,
                    "photo": photo
                })
                serial.is_valid(raise_exception=True)
                obj.append(ProductImage(product=instance, photo=serial.validated_data.get('photo')))
            if obj:
                ProductImage.objects.bulk_create(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductDeleteAPIView(DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductCreateSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'guid'
