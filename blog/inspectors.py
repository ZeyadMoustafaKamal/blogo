from drf_yasg.inspectors import FieldInspector
from drf_yasg import openapi
from rest_framework.fields import UUIDField

class UUIDFieldInspector(FieldInspector):
    def field_to_swagger_object(self, field):
        swagger_object = super().field_to_swagger_object(field)
        if isinstance(field, UUIDField):
            swagger_object.update({
                'type': openapi.TYPE_STRING,
                'format': openapi.FORMAT_UUID,
            })
        return swagger_object



