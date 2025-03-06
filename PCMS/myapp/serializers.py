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

#=================================================================Firmware=======================================================

from rest_framework import serializers
from .models import FirmwareTestReport

class FirmwareTestReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = FirmwareTestReport
        fields = '__all__'

#=================================================================FirmwareDriverDocument=======================================================

from rest_framework import serializers
from .models import FirmwareDriverDocument

class FirmwareDriverDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FirmwareDriverDocument
        fields = '__all__'


#=============================================FirmwareLowLevelDesign=======================================================

from rest_framework import serializers
from .models import FirmwareLowLevelDesign

class FirmwareLowLevelDesignSerializer(serializers.ModelSerializer):
    class Meta:
        model = FirmwareLowLevelDesign
        fields = '__all__'
#====================================================FirmwareProtocolDocument========================================

from rest_framework import serializers
from .models import FirmwareProtocolDocument

class FirmwareProtocolDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FirmwareProtocolDocument
        fields = '__all__'
# ===============================RS485 Modbus Protocol Document===================================================

from rest_framework import serializers
from .models import RS485ModbusProtocolDocument

class RS485ModbusProtocolDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = RS485ModbusProtocolDocument
        fields = '__all__'


#==================================== High-Level Design Document details ======================================

from rest_framework import serializers
from .models import HighLevelDesignDocument

class HighLevelDesignDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = HighLevelDesignDocument
        fields = '__all__'
#===================================== Software High-Level Design Document details =================================

from rest_framework import serializers
from .models import SoftwareHLDDocument

class SoftwareHLDDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoftwareHLDDocument
        fields = '__all__'
#===================================== Software Low-Level Design (LLD) Document =================================

from rest_framework import serializers
from .models import SoftwareLLDDocument

class SoftwareLLDDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoftwareLLDDocument
        fields = '__all__'


#============================================= Software Requirements Specification (SRS) Document=======================


from rest_framework import serializers
from .models import SoftwareSRS

class SoftwareSRSSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoftwareSRS
        fields = '__all__'


#==============================Software Test Specification Document details=======================================

from rest_framework import serializers
from .models import SoftwareTestSpecification

class SoftwareTestSpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoftwareTestSpecification
        fields = '__all__'



#================================================ Hardware Low-Level Design (LLD) Document details.==========================
from rest_framework import serializers
from .models import HardwareLLD, TestCaseLLD, IssueObservationLLD

class TestCaseLLDSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCaseLLD
        exclude = ['hardware_lld']  # Exclude hardware_lld to avoid "This field is required" error

class IssueObservationLLDSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssueObservationLLD
        exclude = ['hardware_lld']  # Exclude hardware_lld to avoid "This field is required" error

class HardwareLLDSerializer(serializers.ModelSerializer):
    test_cases = TestCaseLLDSerializer(many=True, required=False)
    issues = IssueObservationLLDSerializer(many=True, required=False)

    class Meta:
        model = HardwareLLD
        fields = '__all__'

    def create(self, validated_data):
        test_cases_data = validated_data.pop('test_cases', [])
        issues_data = validated_data.pop('issues', [])

        # ✅ Create Hardware LLD entry first
        hardware_lld = HardwareLLD.objects.create(**validated_data)

        # ✅ Insert Test Cases linked to this Hardware LLD
        for test_case in test_cases_data:
            TestCaseLLD.objects.create(hardware_lld=hardware_lld, **test_case)

        # ✅ Insert Issues linked to this Hardware LLD
        for issue in issues_data:
            IssueObservationLLD.objects.create(hardware_lld=hardware_lld, **issue)

        return hardware_lld

    def update(self, instance, validated_data):
        test_cases_data = validated_data.pop('test_cases', [])
        issues_data = validated_data.pop('issues', [])

        instance.project_name = validated_data.get('project_name', instance.project_name)
        instance.version = validated_data.get('version', instance.version)
        instance.date = validated_data.get('date', instance.date)
        instance.prepared_by = validated_data.get('prepared_by', instance.prepared_by)
        instance.reviewed_by = validated_data.get('reviewed_by', instance.reviewed_by)
        instance.approved_by = validated_data.get('approved_by', instance.approved_by)
        instance.purpose = validated_data.get('purpose', instance.purpose)
        instance.scope = validated_data.get('scope', instance.scope)
        instance.references = validated_data.get('references', instance.references)
        instance.block_diagram = validated_data.get('block_diagram', instance.block_diagram)
        instance.test_equipment_used = validated_data.get('test_equipment_used', instance.test_equipment_used)
        instance.operating_conditions = validated_data.get('operating_conditions', instance.operating_conditions)
        instance.conclusion = validated_data.get('conclusion', instance.conclusion)
        instance.suggested_fixes = validated_data.get('suggested_fixes', instance.suggested_fixes)
        instance.additional_tests = validated_data.get('additional_tests', instance.additional_tests)
        instance.approval_status = validated_data.get('approval_status', instance.approval_status)
        instance.approver_name = validated_data.get('approver_name', instance.approver_name)
        instance.approval_date = validated_data.get('approval_date', instance.approval_date)
        instance.save()

        return instance
    
    
    #========================================Low-Level Design (LLD) Document details.===================================

from rest_framework import serializers
from .models import LowLevelDesignFunctional, TestCaseFunctionalLLD

class TestCaseFunctionalLLDSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCaseFunctionalLLD
        exclude = ['lld_document']  # Exclude to avoid "This field is required" error

class LowLevelDesignFunctionalSerializer(serializers.ModelSerializer):
    test_cases = TestCaseFunctionalLLDSerializer(many=True, required=False)

    class Meta:
        model = LowLevelDesignFunctional
        fields = '__all__'

    def create(self, validated_data):
        test_cases_data = validated_data.pop('test_cases', [])

        # ✅ Create LLD entry first
        lld_document = LowLevelDesignFunctional.objects.create(**validated_data)

        # ✅ Insert Test Cases linked to this LLD
        for test_case in test_cases_data:
            TestCaseFunctionalLLD.objects.create(lld_document=lld_document, **test_case)

        return lld_document

    def update(self, instance, validated_data):
        test_cases_data = validated_data.pop('test_cases', [])

        instance.project_name = validated_data.get('project_name', instance.project_name)
        instance.version = validated_data.get('version', instance.version)
        instance.date = validated_data.get('date', instance.date)
        instance.prepared_by = validated_data.get('prepared_by', instance.prepared_by)
        instance.reviewed_by = validated_data.get('reviewed_by', instance.reviewed_by)
        instance.approved_by = validated_data.get('approved_by', instance.approved_by)
        instance.purpose = validated_data.get('purpose', instance.purpose)
        instance.scope = validated_data.get('scope', instance.scope)
        instance.references = validated_data.get('references', instance.references)
        instance.overview = validated_data.get('overview', instance.overview)
        instance.module_specifications = validated_data.get('module_specifications', instance.module_specifications)
        instance.microcontroller_processor = validated_data.get('microcontroller_processor', instance.microcontroller_processor)
        instance.memory_map = validated_data.get('memory_map', instance.memory_map)
        instance.peripheral_interfaces = validated_data.get('peripheral_interfaces', instance.peripheral_interfaces)
        instance.power_management = validated_data.get('power_management', instance.power_management)
        instance.firmware_architecture = validated_data.get('firmware_architecture', instance.firmware_architecture)
        instance.task_scheduling = validated_data.get('task_scheduling', instance.task_scheduling)
        instance.interrupt_handling = validated_data.get('interrupt_handling', instance.interrupt_handling)
        instance.data_structures_algorithms = validated_data.get('data_structures_algorithms', instance.data_structures_algorithms)
        instance.error_handling_debugging = validated_data.get('error_handling_debugging', instance.error_handling_debugging)
        instance.internal_communication = validated_data.get('internal_communication', instance.internal_communication)
        instance.external_communication = validated_data.get('external_communication', instance.external_communication)
        instance.security_features = validated_data.get('security_features', instance.security_features)
        instance.safety_mechanisms = validated_data.get('safety_mechanisms', instance.safety_mechanisms)
        instance.timing_constraints = validated_data.get('timing_constraints', instance.timing_constraints)
        instance.resource_utilization = validated_data.get('resource_utilization', instance.resource_utilization)
        instance.unit_testing = validated_data.get('unit_testing', instance.unit_testing)
        instance.integration_testing = validated_data.get('integration_testing', instance.integration_testing)
        instance.validation_criteria = validated_data.get('validation_criteria', instance.validation_criteria)
        instance.version_date = validated_data.get('version_date', instance.version_date)
        instance.author_changes = validated_data.get('author_changes', instance.author_changes)
        instance.save()

        return instance
# ===========================================Milestone Schedule Chart================================================


from rest_framework import serializers
from .models import MilestoneSchedule, Milestone

class MilestoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Milestone
        exclude = ['milestone_schedule']  # Exclude to avoid "This field is required" error

class MilestoneScheduleSerializer(serializers.ModelSerializer):
    milestones = MilestoneSerializer(many=True, required=False)

    class Meta:
        model = MilestoneSchedule
        fields = '__all__'

    def create(self, validated_data):
        milestones_data = validated_data.pop('milestones', [])

        # ✅ Create the Milestone Schedule Document
        schedule = MilestoneSchedule.objects.create(**validated_data)

        # ✅ Insert Milestones linked to this schedule
        for milestone in milestones_data:
            Milestone.objects.create(milestone_schedule=schedule, **milestone)

        return schedule

    def update(self, instance, validated_data):
        milestones_data = validated_data.pop('milestones', [])

        instance.project_name = validated_data.get('project_name', instance.project_name)
        instance.version = validated_data.get('version', instance.version)
        instance.date = validated_data.get('date', instance.date)
        instance.prepared_by = validated_data.get('prepared_by', instance.prepared_by)
        instance.reviewed_by = validated_data.get('reviewed_by', instance.reviewed_by)
        instance.approved_by = validated_data.get('approved_by', instance.approved_by)
        instance.purpose = validated_data.get('purpose', instance.purpose)
        instance.scope = validated_data.get('scope', instance.scope)
        instance.dependencies_risks = validated_data.get('dependencies_risks', instance.dependencies_risks)
        instance.version_date = validated_data.get('version_date', instance.version_date)
        instance.author_changes = validated_data.get('author_changes', instance.author_changes)
        instance.save()

        return instance

#==================================   User Acceptance Test (UAT) Document ========================

from rest_framework import serializers
from .models import UATDocument, UATTestCase

class UATTestCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UATTestCase
        exclude = ['uat_document']  # Exclude to avoid "This field is required" error

class UATDocumentSerializer(serializers.ModelSerializer):
    test_cases = UATTestCaseSerializer(many=True, required=False)

    class Meta:
        model = UATDocument
        fields = '__all__'

    def create(self, validated_data):
        test_cases_data = validated_data.pop('test_cases', [])

        # ✅ Create the UAT Document
        uat_document = UATDocument.objects.create(**validated_data)

        # ✅ Insert Test Cases linked to this UAT Document
        for test_case in test_cases_data:
            UATTestCase.objects.create(uat_document=uat_document, **test_case)

        return uat_document

    def update(self, instance, validated_data):
        test_cases_data = validated_data.pop('test_cases', [])

        instance.project_name = validated_data.get('project_name', instance.project_name)
        instance.version = validated_data.get('version', instance.version)
        instance.test_date = validated_data.get('test_date', instance.test_date)
        instance.prepared_by = validated_data.get('prepared_by', instance.prepared_by)
        instance.reviewed_by = validated_data.get('reviewed_by', instance.reviewed_by)
        instance.approved_by = validated_data.get('approved_by', instance.approved_by)
        instance.purpose = validated_data.get('purpose', instance.purpose)
        instance.scope = validated_data.get('scope', instance.scope)
        instance.references = validated_data.get('references', instance.references)
        instance.overview = validated_data.get('overview', instance.overview)
        instance.assumptions = validated_data.get('assumptions', instance.assumptions)
        instance.test_environment = validated_data.get('test_environment', instance.test_environment)
        instance.hardware_design = validated_data.get('hardware_design', instance.hardware_design)
        instance.defect_logging = validated_data.get('defect_logging', instance.defect_logging)
        instance.resolution_process = validated_data.get('resolution_process', instance.resolution_process)
        instance.test_results_summary = validated_data.get('test_results_summary', instance.test_results_summary)
        instance.acceptance_decision = validated_data.get('acceptance_decision', instance.acceptance_decision)
        instance.version_date = validated_data.get('version_date', instance.version_date)
        instance.author_changes = validated_data.get('author_changes', instance.author_changes)
        instance.save()

        return instance

