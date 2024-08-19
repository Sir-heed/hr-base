from rest_framework.serializers import ModelSerializer


class ModelSerializer(ModelSerializer):
    """
    Common Model serializer

    .. note:: Extends from :class:`rest_framework.serializers.ModelSerializer`
    """

    def before_validate(self, attrs):
        return attrs

    def before_instance(self, attrs):
        return attrs

    def clean_instance(self, instance):
        instance.full_clean()

    def validate(self, attrs):
        """
        Call Model’s full_clean() method to ensure model-level-validation
        """

        cleaned_data = super().validate(self.before_validate(attrs))

        # Use existing instance to avoid issues with partial updates
        instance = self.instance or self.Meta.model()
        for key, value in self.before_instance(cleaned_data).items():
            setattr(instance, key, value)

        self.clean_instance(instance)
        return cleaned_data

    class Meta:
        read_only_fields = ['is_active', 'created', 'modified']
        exclude = []
