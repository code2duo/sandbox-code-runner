from rest_framework import serializers


class CompilerSerializer(serializers.Serializer):
    """
    Serializer class for Compiler Endpoint (essentially)
    """

    LanguageChoices = [
        ("python", "python"),
    ]

    userid = serializers.CharField(max_length=8)
    language = serializers.ChoiceField(choices=LanguageChoices)
    source = serializers.CharField(max_length=1000)
    timeout = serializers.IntegerField(min_value=1, max_value=15)
