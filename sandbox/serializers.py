from rest_framework import serializers


class CompilerSerializer(serializers.Serializer):
    """
    Serializer class for Compiler Endpoint (essentially)
    """

    LanguageChoices = [
        ("python", "python"),
        ("c", "c"),
        ("cpp", "cpp"),
    ]

    userid = serializers.CharField(max_length=8)
    language = serializers.ChoiceField(choices=LanguageChoices)
    source = serializers.CharField(max_length=10000)
    timeout = serializers.IntegerField(min_value=1, max_value=15)
