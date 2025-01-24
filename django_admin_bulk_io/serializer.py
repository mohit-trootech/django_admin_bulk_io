from rest_framework.serializers import ModelSerializer


class BulkIODynamicSerializer(ModelSerializer):

    class Meta:
        model = None
        fields = "__all__"


# >>> s.data
# [{'id': 3, 'title': 'eg', 'description': 'ehwh', 'comment': 13710, 'likes': [1]}, {'id': 4, 'title': '5w4h4', 'description': 'hwe5hw45', 'comment': 13713, 'likes': [1, 2]}]
