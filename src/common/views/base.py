from rest_framework import viewsets


class BaseViewSet(viewsets.ModelViewSet):

    def get_serializer(self, *args, **kwargs):
        if "data" in kwargs:
            data = kwargs["data"]
            if isinstance(data, list):
                kwargs["many"] = True
        return super(BaseViewSet, self).get_serializer(*args, **kwargs)
