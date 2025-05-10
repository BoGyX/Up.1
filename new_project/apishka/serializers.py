from rest_framework import serializers
from hello.models import User, Category, Manufacturer, Artist, VinylRecord, Order, Cart, CartItem, OrderDetail

# Сериализатор для Category
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

# Сериализатор для Manufacturer
class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = ['id', 'name']

# Сериализатор для Artist
class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ['id', 'name']

# Сериализатор для VinylRecord
class VinylRecordSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer(read_only=True)  # Включаем данные об исполнителе
    category = CategorySerializer(read_only=True)  # Включаем данные о категории
    manufacturer = ManufacturerSerializer(read_only=True)  # Включаем данные о производителе
    artist_id = serializers.PrimaryKeyRelatedField(
        queryset=Artist.objects.all(), source='artist', write_only=True
    )  # Для записи используем ID
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )
    manufacturer_id = serializers.PrimaryKeyRelatedField(
        queryset=Manufacturer.objects.all(), source='manufacturer', write_only=True
    )

    class Meta:
        model = VinylRecord
        fields = [
            'id', 'title', 'artist', 'artist_id', 'category', 'category_id',
            'manufacturer', 'manufacturer_id', 'price', 'image_url'
        ]

# Сериализатор для User (ограниченный для безопасности)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'login', 'name', 'surname', 'middle_name', 'is_active']
        read_only_fields = ['is_active', 'is_staff', 'is_superuser']

# Сериализатор для CartItem
class CartItemSerializer(serializers.ModelSerializer):
    vinyl = VinylRecordSerializer(read_only=True)  # Включаем данные о товаре
    vinyl_id = serializers.PrimaryKeyRelatedField(
        queryset=VinylRecord.objects.all(), source='vinyl', write_only=True
    )  # Для записи используем ID
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'vinyl', 'vinyl_id', 'quantity', 'subtotal', 'created_at', 'updated_at']

# Сериализатор для Cart
class CartSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # Включаем данные о пользователе
    items = CartItemSerializer(many=True, read_only=True)  # Включаем элементы корзины
    total = serializers.SerializerMethodField()  # Вычисляем общую сумму

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total', 'created_at', 'updated_at']

    def get_total(self, obj):
        return sum(item.subtotal for item in obj.items.all())

# Сериализатор для OrderDetail
class OrderDetailSerializer(serializers.ModelSerializer):
    vinyl = VinylRecordSerializer(read_only=True)
    vinyl_id = serializers.PrimaryKeyRelatedField(
        queryset=VinylRecord.objects.all(), source='vinyl', write_only=True
    )

    class Meta:
        model = OrderDetail
        fields = ['id', 'vinyl', 'vinyl_id', 'quantity', 'price']

# Сериализатор для Order
class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    details = OrderDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'total_price', 'details']

# Сериализатор для добавления/обновления CartItem (для API операций с корзиной)
class CartItemAddSerializer(serializers.Serializer):
    vinyl_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1, default=1)

    def validate_vinyl_id(self, value):
        if not VinylRecord.objects.filter(id=value).exists():
            raise serializers.ValidationError("Товар с таким ID не существует")
        return value

# Сериализатор для регистрации пользователя
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['login', 'password', 'name', 'surname', 'middle_name']

    def create(self, validated_data):
        user = User.objects.create_user(
            login=validated_data['login'],
            password=validated_data['password'],
            name=validated_data['name'],
            surname=validated_data['surname'],
            middle_name=validated_data['middle_name']
        )
        # Создаём корзину для нового пользователя
        Cart.objects.get_or_create(user=user)
        return user