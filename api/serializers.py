from rest_framework import serializers, exceptions

from api.models import Book, Publish


class PressModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Publish
        fields = ("pub_name", "address", "pic")


class BookModelSerializer(serializers.ModelSerializer):

    publish = PressModelSerializer()

    class Meta:

        model = Book
        fields = ("book_name", "price", "pic", "publish")

        # fields = "__all__"

        # exclude = ("is_delete", "create_time", "status")

        # depth = 1


class BookDeModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = ("book_name", "price", "publish", "authors")

        # 添加DRF所提供的校验规则
        extra_kwargs = {
            "book_name": {
                "required": True,
                "min_length": 3,
                "error_messages": {
                    "required": "图书名是必填的",
                    "min_length": "长度不够，太短了哦~"
                }
            },
            "price": {
                "max_digits": 5,
                "decimal_places": 2,
            }
        }

    def validate_book_name(self, value):
        # 自定义用户名校验规则
        if "1" in value:
            raise exceptions.ValidationError("图书名含有敏感字")
        return value

    # 全局校验钩子
    def validate(self, attrs):
        price = attrs.get("price", 0)
        if price > 90:
            raise exceptions.ValidationError("超过设定的最高价钱~")

        return attrs


class BookModelSerializerTogether(serializers.ModelSerializer):
    class Meta:
        model = Book
        # fields应该填写哪些字段  应该填写序列化与反序列化字段的并集
        fields = ("book_name", "price", "publish", "authors", "pic")

        # 添加DRF所提供的校验规则
        extra_kwargs = {
            "book_name": {
                "required": True,
                "min_length": 3,
                "error_messages": {
                    "required": "图书名是必填的",
                    "min_length": "长度不够，太短啦~"
                }
            },
            # 指定此字段只参与反序列化
            "publish": {
                "write_only": True
            },
            "authors": {
                "write_only": True
            },
            # 指定此字段只参与序列化
            "pic": {
                "read_only": True
            }
        }

    def validate_book_name(self, value):
        # 自定义用户名校验规则
        if "1" in value:
            raise exceptions.ValidationError("图书名含有敏感字")
        return value

    # 全局校验钩子
    def validate(self, attrs):

        price = attrs.get("price", 0)
        if price > 90:
            raise exceptions.ValidationError("超过设定的最高价钱~")

        return attrs
