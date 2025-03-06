
from django.db import models

class HardwareTestReport(models.Model):
    project_name = models.CharField(max_length=255)
    test_date = models.DateField()
    tested_by = models.CharField(max_length=255)

class TestEnvironment(models.Model):
    report = models.ForeignKey(HardwareTestReport, on_delete=models.CASCADE, related_name='environment')
    hardware_version = models.CharField(max_length=50)
    firmware_version = models.CharField(max_length=50)
    test_equipment_used = models.TextField()
    operating_conditions = models.TextField()

class TestCase(models.Model):
    report = models.ForeignKey(HardwareTestReport, on_delete=models.CASCADE, related_name='test_cases')
    test_case_no = models.IntegerField()
    test_description = models.TextField()
    expected_outcome = models.TextField()
    actual_outcome = models.TextField()
    status = models.CharField(max_length=10, choices=[('Pass', 'Pass'), ('Fail', 'Fail')])

class IssueObservation(models.Model):
    report = models.ForeignKey(HardwareTestReport, on_delete=models.CASCADE, related_name='issues')
    issue_description = models.TextField()
    suggested_resolution = models.TextField()

class ConclusionRecommendation(models.Model):
    report = models.ForeignKey(HardwareTestReport, on_delete=models.CASCADE, related_name='conclusion')
    summary = models.TextField()
    next_steps = models.TextField()
    approved_by = models.CharField(max_length=255)
    approval_date = models.DateField()
#======================================================Firmware API Document=============================================== 

from django.db import models

class FirmwareTestReport(models.Model):
    project_name = models.CharField(max_length=255)
    firmware_version = models.CharField(max_length=50)
    test_date = models.DateField()
    author = models.CharField(max_length=255)

    # Introduction Section
    objective = models.TextField()
    scope = models.TextField()
    references = models.TextField()

    # API Overview
    architecture = models.TextField()
    dependencies = models.TextField()

    # API Functions
    gpio_api = models.TextField()
    uart_api = models.TextField()
    timer_api = models.TextField()
    adc_api = models.TextField()
    spi_api = models.TextField()
    i2c_api = models.TextField()

    # Other Sections
    error_handling = models.TextField()
    usage_examples = models.TextField()
    testing_validation = models.TextField()
    conclusion = models.TextField()

    # Approval Section
    approver_name = models.CharField(max_length=255)
    approval_date = models.DateField()

    def __str__(self):
        return f"{self.project_name} - {self.firmware_version}"
    
    
    class Meta:
        db_table = 'API_Firmware API Document'


#======================================================Firmware Driver Document=========================================

from django.db import models

class FirmwareDriverDocument(models.Model):
    project_name = models.CharField(max_length=255)
    firmware_version = models.CharField(max_length=50)
    test_date = models.DateField()
    author = models.CharField(max_length=255)

    # Introduction Section
    objective = models.TextField()
    scope = models.TextField()
    references = models.TextField()

    # System Overview
    microcontroller = models.TextField()
    architecture = models.TextField()

    # Driver Modules
    gpio_driver = models.TextField()
    uart_protocol = models.TextField()
    timer_driver = models.TextField()
    adc_driver = models.TextField()
    spi_driver = models.TextField()
    i2c_driver = models.TextField()

    # Other Sections
    error_handling = models.TextField()
    test_validation = models.TextField()
    conclusion = models.TextField()

    # Approval Section
    approver_name = models.CharField(max_length=255)
    approval_date = models.DateField()

    def __str__(self):
        return f"{self.project_name} - {self.firmware_version}"
    
    class Meta:
        db_table = 'API_Firmware Driver Document'

#=============================================FirmwareLowLevelDesign=======================================================
from django.db import models

class FirmwareLowLevelDesign(models.Model):
    project_name = models.CharField(max_length=255)
    firmware_version = models.CharField(max_length=50)
    test_date = models.DateField()
    author = models.CharField(max_length=255)

    # Introduction Section
    objective = models.TextField()
    scope = models.TextField()
    references = models.TextField()

    # System Architecture
    hardware_overview = models.TextField()
    firmware_structure = models.TextField()

    # Boot Process
    startup_sequence = models.TextField()
    bootloader = models.TextField()

    # Modules & Drivers
    gpio_driver = models.TextField()
    uart_driver = models.TextField()
    timer_driver = models.TextField()
    adc_driver = models.TextField()
    other_peripherals = models.TextField()

    # Additional Sections
    task_management = models.TextField()
    error_handling = models.TextField()
    memory_management = models.TextField()
    security_considerations = models.TextField()
    conclusion = models.TextField()

    # Approval Section
    approver_name = models.CharField(max_length=255)
    approval_date = models.DateField()

    def __str__(self):
        return f"{self.project_name} - {self.firmware_version}"
    
    class Meta:
        db_table = 'API_FirmwareLowLevelDesign'



#====================================================FirmwareProtocolDocument========================================

from django.db import models

class FirmwareProtocolDocument(models.Model):
    project_name = models.CharField(max_length=255)
    firmware_version = models.CharField(max_length=50)
    test_date = models.DateField()
    author = models.CharField(max_length=255)

    # Introduction Section
    objective = models.TextField()
    scope = models.TextField()
    references = models.TextField()

    # Communication Overview
    supported_protocols = models.TextField()
    data_transmission_modes = models.TextField()

    # Protocol Specifications
    uart_protocol = models.TextField()
    spi_protocol = models.TextField()
    i2c_protocol = models.TextField()
    can_protocol = models.TextField()

    # Other Sections
    message_structure = models.TextField()
    error_handling = models.TextField()
    security_considerations = models.TextField()
    conclusion = models.TextField()

    # Approval Section
    approver_name = models.CharField(max_length=255)
    approval_date = models.DateField()

    def __str__(self):
        return f"{self.project_name} - {self.firmware_version}"
    
    class Meta:
        db_table = 'API_Firmware Protocol Document'
        
        
# ===============================RS485 Modbus Protocol Document===================================================

from django.db import models

class RS485ModbusProtocolDocument(models.Model):
    project_name = models.CharField(max_length=255)
    firmware_version = models.CharField(max_length=50)
    test_date = models.DateField()
    prepared_by = models.CharField(max_length=255)
    author = models.CharField(max_length=255)

    # Introduction Section
    objective = models.TextField()
    scope = models.TextField()
    references = models.TextField()

    # Communication Overview
    protocol_type = models.TextField()
    transmission_mode = models.TextField()
    data_transmission_modes = models.TextField()

    # Protocol Specifications
    rs485_physical_layer = models.TextField()
    modbus_rtu_frame_format = models.TextField()
    modbus_ascii_frame_format = models.TextField()

    # Other Sections
    function_codes = models.TextField()
    error_handling = models.TextField()
    security_considerations = models.TextField()
    conclusion = models.TextField()

    # Approval Section
    approver_name = models.CharField(max_length=255)
    approval_date = models.DateField()

    def __str__(self):
        return f"{self.project_name} - {self.firmware_version}"
    
    class Meta:
        db_table = 'API_RS485 Modbus Protocol Document'

        
#==================================== High-Level Design Document details ======================================


from django.db import models

class HighLevelDesignDocument(models.Model):
    project_name = models.CharField(max_length=255)
    version = models.CharField(max_length=50)
    date = models.DateField()
    prepared_by = models.CharField(max_length=255)
    reviewed_by = models.CharField(max_length=255)
    approved_by = models.CharField(max_length=255)

    # Introduction Section
    purpose = models.TextField()
    scope = models.TextField()
    references = models.TextField()

    # System Architecture
    system_description = models.TextField()
    block_diagram = models.TextField()
    key_functionalities = models.TextField()

    # Design Inputs
    functional_requirements = models.TextField()
    performance_requirements = models.TextField()
    hardware_requirements = models.TextField()
    software_requirements = models.TextField()
    environmental_requirements = models.TextField()
    regulatory_compliance = models.TextField()
    safety_protection = models.TextField()

    # Constraints & Assumptions
    design_constraints = models.TextField()
    assumptions = models.TextField()

    # Risk Analysis
    risk_analysis = models.TextField()

    # Revision History
    version_date = models.DateField()
    author_changes = models.TextField()

    def __str__(self):
        return f"{self.project_name} - {self.version}"
    
    class Meta:
        db_table = 'API_High-Level Design Document details'


#===================================== Software High-Level Design Document details =================================

from django.db import models

class SoftwareHLDDocument(models.Model):
    # Introduction Section
    purpose = models.TextField()
    scope = models.TextField()
    definitions_acronyms_abbreviations = models.TextField()
    references = models.TextField()

    # System Overview
    system_purpose_objectives = models.TextField()
    high_level_architecture = models.TextField()
    system_context = models.TextField()

    # Architecture and Design
    architectural_style = models.TextField()
    component_design = models.TextField()
    data_flow = models.TextField()
    communication_integration = models.TextField()

    # UI/UX Design (if applicable)
    user_interface_overview = models.TextField()
    interaction_design = models.TextField()

    # Data Design
    database_overview = models.TextField()
    data_flow_processing = models.TextField()
    data_security = models.TextField()

    # Non-Functional Requirements
    performance = models.TextField()
    security = models.TextField()
    availability_reliability = models.TextField()
    scalability = models.TextField()
    maintainability = models.TextField()

    # External Interfaces
    user_interfaces = models.TextField()
    hardware_interfaces = models.TextField()
    software_interfaces = models.TextField()

    # Deployment and Hosting
    deployment_architecture = models.TextField()
    hardware_network_requirements = models.TextField()

    # Appendix
    glossary = models.TextField()
    diagrams = models.TextField()

    def __str__(self):
        return f"Software HLD Document - {self.id}"
    

    class Meta:
        db_table = "API_softwarehlddocument"  
    
    
#===================================== Software Low-Level Design (LLD) Document =================================


from django.db import models

class SoftwareLLDDocument(models.Model):
    # Introduction Section
    purpose = models.TextField()
    scope = models.TextField()
    definitions_acronyms_abbreviations = models.TextField()
    references = models.TextField()

    # Design Overview
    architectural_design = models.TextField()
    design_constraints = models.TextField()
    assumptions_dependencies = models.TextField()

    # Module-Level Design
    module_purpose = models.TextField()
    module_interfaces = models.TextField()
    component_design = models.TextField()
    data_flow = models.TextField()
    error_handling = models.TextField()
    performance_considerations = models.TextField()
    security_considerations = models.TextField()
    unit_tests = models.TextField()

    # Database Design
    database_overview = models.TextField()
    database_schema = models.TextField()
    data_access_layer_design = models.TextField()

    # Communication Protocols
    internal_communication = models.TextField()
    external_communication = models.TextField()

    # Integration Design
    integration_external_systems = models.TextField()
    integration_other_modules = models.TextField()

    # UI/UX Design (if applicable)
    user_interface_components = models.TextField()
    ui_logic = models.TextField()

    # Testing and Quality Assurance
    unit_testing_strategy = models.TextField()
    integration_testing = models.TextField()
    performance_testing = models.TextField()
    code_reviews_static_analysis = models.TextField()

    # Appendix
    appendix = models.TextField()

    def __str__(self):
        return f"Software LLD Document - {self.id}"
    
    class Meta:
        db_table = "API_SoftwareLLDDocument" 


#============================================= Software Requirements Specification (SRS) Document=======================

from django.db import models

class SoftwareSRS(models.Model):
    # Document Metadata
    project_name = models.CharField(max_length=255)
    version = models.CharField(max_length=50)
    date = models.DateField()
    prepared_by = models.CharField(max_length=255)
    reviewed_by = models.CharField(max_length=255)
    approved_by = models.CharField(max_length=255)

    # Introduction Section
    purpose = models.TextField()
    scope = models.TextField()
    definitions_acronyms_abbreviations = models.TextField()
    references = models.TextField()
    overview = models.TextField()

    # Overall Description
    product_perspective = models.TextField()
    user_classes_characteristics = models.TextField()
    operating_environment = models.TextField()
    design_implementation_constraints = models.TextField()
    assumptions_dependencies = models.TextField()

    # System Features
    hardware_design = models.TextField()

    # External Interface Requirements
    user_interfaces = models.TextField()
    hardware_interfaces = models.TextField()
    software_interfaces = models.TextField()
    communication_interfaces = models.TextField()

    # System Attributes
    reliability = models.TextField()
    availability = models.TextField()
    security = models.TextField()
    maintainability = models.TextField()
    portability = models.TextField()

    # Other Non-Functional Requirements
    performance = models.TextField()
    scalability = models.TextField()
    usability = models.TextField()
    legal_regulatory = models.TextField()

    # Appendix
    appendix = models.TextField()

    def __str__(self):
        return f"{self.project_name} - {self.version}"
    
    class Meta:
        db_table = "API_Software Requirements Specification (SRS) Document" 


#==============================Software Test Specification Document details=======================================


class SoftwareTestSpecification(models.Model):
    # Introduction Section
    purpose = models.TextField()
    scope = models.TextField()
    test_objectives = models.TextField()
    definitions_acronyms_abbreviations = models.TextField()
    references = models.TextField()

    # Test Strategy
    test_levels = models.TextField()
    test_types = models.TextField()
    test_approach = models.TextField()
    test_environment = models.TextField()

    # Test Scope
    features_to_be_tested = models.TextField()
    features_not_to_be_tested = models.TextField()

    # Test Criteria
    entry_criteria = models.TextField()
    exit_criteria = models.TextField()

    # Test Plan
    test_cases = models.TextField()
    test_execution_schedule = models.TextField()
    resource_requirements = models.TextField()

    # Defect Management
    defect_reporting = models.TextField()
    defect_lifecycle = models.TextField()
    severity_priority = models.TextField()

    # Risks and Mitigations
    risks = models.TextField()
    mitigation_strategies = models.TextField()

    # Test Deliverables
    test_reports = models.TextField()
    test_logs = models.TextField()
    test_artifacts = models.TextField()

    # Appendix
    appendix = models.TextField()

    def __str__(self):
        return f"Software Test Specification Document - {self.id}"
    
    
 #================================================ Hardware Low-Level Design (LLD) Document details.==========================
from django.db import models

class HardwareLLD(models.Model):
    # Document Metadata
    project_name = models.CharField(max_length=255)
    version = models.CharField(max_length=50)
    date = models.DateField()
    prepared_by = models.CharField(max_length=255)
    reviewed_by = models.CharField(max_length=255)
    approved_by = models.CharField(max_length=255)

    # Introduction Section
    purpose = models.TextField()
    scope = models.TextField()
    references = models.TextField()

    # System Overview
    block_diagram = models.TextField()
    test_equipment_used = models.TextField()
    operating_conditions = models.TextField()

    # Conclusion & Recommendations
    conclusion = models.TextField()
    suggested_fixes = models.TextField()
    additional_tests = models.TextField()
    approval_status = models.TextField()
    approver_name = models.CharField(max_length=255)
    approval_date = models.DateField()

    def __str__(self):
        return f"{self.project_name} - {self.version}"

    class Meta:
        db_table = "API_HardwareLLD"


class TestCaseLLD(models.Model):
    hardware_lld = models.ForeignKey(HardwareLLD, on_delete=models.CASCADE, related_name="test_cases")
    test_case_no = models.IntegerField()
    test_description = models.TextField()
    expected_outcome = models.TextField()
    actual_outcome = models.TextField()
    status = models.CharField(max_length=10, choices=[("Pass", "Pass"), ("Fail", "Fail")])

    def __str__(self):
        return f"Test Case {self.test_case_no} - {self.hardware_lld.project_name}"

    class Meta:
        db_table = "API_HardwareLLD_TestCase"


class IssueObservationLLD(models.Model):
    hardware_lld = models.ForeignKey(HardwareLLD, on_delete=models.CASCADE, related_name="issues")
    issue_description = models.TextField()

    def __str__(self):
        return f"Issue - {self.hardware_lld.project_name}"

    class Meta:
        db_table = "API_HardwareLLD_IssueObservation"



#========================================Low-Level Design (LLD) Document details.===================================

from django.db import models

class LowLevelDesignFunctional(models.Model):
    # Document Metadata
    project_name = models.CharField(max_length=255)
    version = models.CharField(max_length=50)
    date = models.DateField()
    prepared_by = models.CharField(max_length=255)
    reviewed_by = models.CharField(max_length=255)
    approved_by = models.CharField(max_length=255)

    # Introduction Section
    purpose = models.TextField()
    scope = models.TextField()
    references = models.TextField()

    # Module Descriptions
    overview = models.TextField()
    module_specifications = models.TextField()

    # Hardware Design
    microcontroller_processor = models.TextField()
    memory_map = models.TextField()
    peripheral_interfaces = models.TextField()
    power_management = models.TextField()

    # Software Design
    firmware_architecture = models.TextField()
    task_scheduling = models.TextField()
    interrupt_handling = models.TextField()
    data_structures_algorithms = models.TextField()
    error_handling_debugging = models.TextField()

    # Interface Details
    internal_communication = models.TextField()
    external_communication = models.TextField()

    # Security & Safety
    security_features = models.TextField()
    safety_mechanisms = models.TextField()

    # Performance Considerations
    timing_constraints = models.TextField()
    resource_utilization = models.TextField()

    # Test Plan & Validation
    unit_testing = models.TextField()
    integration_testing = models.TextField()
    validation_criteria = models.TextField()

    # Revision History
    version_date = models.DateField()
    author_changes = models.TextField()

    def __str__(self):
        return f"{self.project_name} - {self.version}"
    
    class Meta:
        db_table = "API_LowLevelDesign_Functional"


class TestCaseFunctionalLLD(models.Model):
    lld_document = models.ForeignKey(
        LowLevelDesignFunctional,
        on_delete=models.CASCADE,
        related_name="test_cases",
        null=True, blank=True  # Allow NULL for initial migrations
    )
    test_case_no = models.IntegerField()
    test_description = models.TextField()
    expected_outcome = models.TextField()
    actual_outcome = models.TextField()
    status = models.CharField(max_length=10, choices=[("Pass", "Pass"), ("Fail", "Fail")])

    def __str__(self):
        return f"Test Case {self.test_case_no} - {self.lld_document.project_name if self.lld_document else 'No LLD'}"

    class Meta:
        db_table = "API_LLD_Functional_TestCase"
        
        
        
# ===========================================Milestone Schedule Chart================================================



class MilestoneSchedule(models.Model):
    # Document Metadata
    project_name = models.CharField(max_length=255)
    version = models.CharField(max_length=50)
    date = models.DateField()
    prepared_by = models.CharField(max_length=255)
    reviewed_by = models.CharField(max_length=255)
    approved_by = models.CharField(max_length=255)

    # Introduction Section
    purpose = models.TextField()
    scope = models.TextField()

    # Key Dependencies & Risks
    dependencies_risks = models.TextField()

    # Revision History
    version_date = models.DateField()
    author_changes = models.TextField()

    def __str__(self):
        return f"{self.project_name} - {self.version}"
    
    class Meta:
        db_table = "API_MilestoneSchedule"

class Milestone(models.Model):
    milestone_schedule = models.ForeignKey(
        MilestoneSchedule, on_delete=models.CASCADE, related_name="milestones", null=True, blank=True
    )
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=[("Pending", "Pending"), ("Ongoing", "Ongoing"), ("Completed", "Completed")])

    def __str__(self):
        return f"Milestone: {self.name} ({self.status})"
    
    class Meta:
        db_table = "API_Milestone"
        
        
        
#==================================   User Acceptance Test (UAT) Document ========================

from django.db import models

class UATDocument(models.Model):
    # Document Metadata
    project_name = models.CharField(max_length=255)
    version = models.CharField(max_length=50)
    test_date = models.DateField()
    prepared_by = models.CharField(max_length=255)
    reviewed_by = models.CharField(max_length=255)
    approved_by = models.CharField(max_length=255)

    # Introduction Section
    purpose = models.TextField()
    scope = models.TextField()
    references = models.TextField()

    # UAT Criteria
    overview = models.TextField()
    assumptions = models.TextField()
    test_environment = models.TextField()

    # Test Plan
    hardware_design = models.TextField()

    # Defect Reporting & Resolution
    defect_logging = models.TextField()
    resolution_process = models.TextField()

    # Sign-Off & Approval
    test_results_summary = models.TextField()
    acceptance_decision = models.TextField()

    # Revision History
    version_date = models.DateField()
    author_changes = models.TextField()

    def __str__(self):
        return f"{self.project_name} - {self.version}"
    
    class Meta:
        db_table = "API_UAT_Document"

class UATTestCase(models.Model):
    uat_document = models.ForeignKey(
        UATDocument, on_delete=models.CASCADE, related_name="test_cases", null=True, blank=True
    )
    test_case_id = models.CharField(max_length=50)
    description = models.TextField()
    expected_results = models.TextField()
    actual_results = models.TextField()
    status = models.CharField(max_length=10, choices=[("Pass", "Pass"), ("Fail", "Fail")])

    def __str__(self):
        return f"Test Case {self.test_case_id} - {self.uat_document.project_name if self.uat_document else 'No UAT'}"
    
    class Meta:
        db_table = "API_UAT_Test_Cases"

     
       
