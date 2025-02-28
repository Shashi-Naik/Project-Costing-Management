from rest_framework import serializers
from .models import HardwareTestReport, TestEnvironment, TestCase, IssueObservation, ConclusionRecommendation

class TestEnvironmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestEnvironment
        fields = '__all__'

class TestCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCase
        fields = '__all__'

class IssueObservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssueObservation
        fields = '__all__'

class ConclusionRecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConclusionRecommendation
        fields = '__all__'

class HardwareTestReportSerializer(serializers.ModelSerializer):
    environment = TestEnvironmentSerializer(many=True, read_only=True)
    test_cases = TestCaseSerializer(many=True, read_only=True)
    issues = IssueObservationSerializer(many=True, read_only=True)
    conclusion = ConclusionRecommendationSerializer(many=True, read_only=True)

    class Meta:
        model = HardwareTestReport
        fields = '__all__'

