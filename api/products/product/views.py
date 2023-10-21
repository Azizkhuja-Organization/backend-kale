import base64

from django.core.files.base import ContentFile
from django.db.models import Q, Exists, OuterRef, F
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, ListAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.paginator import CustomPagination
from api.permissions import IsAdmin
from api.products.images.serializers import ProductImageCreateSerializer
from api.products.product.serializers import ProductCreateSerializer, ProductListSerializer, ProductDetailSerializer, \
    ProductUpdateSerializer, Product1CCreateUpdateSerializer, Product1CDestroySerializer
from common.order.models import Wishlist, Comparison, CartProduct
from common.product.models import Product, ProductImage, SubCategory, ProductCornerStatus
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
    def get(self, request, *args, **kwargs):
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
    pagination_class = CustomPagination

    # @method_decorator(cache_page(CACHE_TTL))
    # @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
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

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


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

    # @method_decorator(cache_page(CACHE_TTL))
    # @method_decorator(vary_on_cookie)
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


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


################### 1C ################
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if auth_header and auth_header.startswith('Basic '):
            encoded_credentials = auth_header.split(' ')[1]
            try:
                decoded_credentials = base64.b64decode(encoded_credentials).decode('utf-8')
            except UnicodeDecodeError:
                decoded_credentials = None
            if decoded_credentials:
                username, password = decoded_credentials.split(':')
                if username == 'kaleapi' and password == 'kaleapi':
                    return User.objects.filter(is_superuser=True).first(), None
        raise AuthenticationFailed('Invalid credentials')


class Product1CCreateUpdateAPIView(CreateAPIView):
    serializer_class = Product1CCreateUpdateSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomAuthentication]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Extract the data from the validated serializer
        validated_data = serializer.validated_data
        try:
            for product_data in validated_data["Товары"]:
                code = product_data["Код"]
                product_instance = Product.objects.filter(code=code).first()

                if product_instance:
                    price = product_data.get("Цена")
                    dis = product_data.get("ЦенаСоСкидкой")
                    discount = ((price - dis) / price) * 100 if product_data.get("ЦенаСоСкидкой") else 0
                    # Update the existing product
                    product_instance.title = product_data['Наименование']
                    product_instance.price = price
                    product_instance.discountPrice = dis
                    product_instance.description = product_data['Описание']
                    product_instance.unit = product_data['ЕдиницаИзмерения']
                    product_instance.brand = product_data['ТорговаяМарка']
                    product_instance.size = product_data['Размеры']
                    product_instance.manufacturer = product_data['Производитель']
                    product_instance.quantity = product_data.get("Остаток")
                    product_instance.discount = discount
                    product_instance.cornerStatus = ProductCornerStatus.DISCOUNT if discount else None
                    # Update other fields as needed
                    photo = get_product_photo(code)
                    if photo:
                        photo_data = photo.split(";base64,")[1]
                        photo_content = ContentFile(base64.b64decode(photo_data), name=f"{code}_photo.png")
                        product_instance.photo = photo_content
                    product_instance.save()
                else:
                    price = product_data.get("Цена")
                    dis = product_data.get("ЦенаСоСкидкой")
                    discount = ((price - dis) / price) * 100 if product_data.get("ЦенаСоСкидкой") else 0
                    Product.objects.create(
                        subcategory=None,
                        code=product_data['Код'],
                        title=product_data['Наименование'],
                        description=product_data['Описание'],
                        price=price,
                        discountPrice=product_data.get("ЦенаСоСкидкой"),
                        material=None,
                        unit=product_data['ЕдиницаИзмерения'],
                        file3D=None,
                        brand=product_data['ТорговаяМарка'],
                        size=product_data['Размеры'],
                        manufacturer=product_data['Производитель'],
                        photo=None,
                        quantity=product_data.get("Остаток"),
                        discount=discount,
                        cornerStatus=ProductCornerStatus.DISCOUNT if discount else None
                    )
        except Exception as e:
            return Response(f"Ошибка: {str(e)}", status=status.HTTP_409_CONFLICT)
        return Response(serializer.data, status=status.HTTP_200_OK)


class Product1CDestroyAPIView(CreateAPIView):
    serializer_class = Product1CDestroySerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomAuthentication]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        try:
            for product_data in validated_data["Товары"]:
                code = product_data["Код"]
                Product.objects.filter(code=code).delete()
        except Exception as e:
            return Response(f"Ошибка: {str(e)}", status=status.HTTP_409_CONFLICT)
        return Response(serializer.data, status=status.HTTP_200_OK)
