from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import HardwareTestReport, TestEnvironment, TestCase, IssueObservation, ConclusionRecommendation
from .serializers import HardwareTestReportSerializer

# Serve HTML pages
def report_form(request):
    return render(request, 'Hw_insertform.html')

def report_list(request):
    return render(request, 'Hw_reports.html')

def edit_report(request, report_id):
    return render(request, 'Hw_edit_report.html')

# API: Get all reports
@api_view(['GET'])
def get_reports(request):
    reports = HardwareTestReport.objects.all()
    serializer = HardwareTestReportSerializer(reports, many=True)
    return Response(serializer.data)

# API: Get a single report
@api_view(['GET'])
def get_report_by_id(request, report_id):
    report = get_object_or_404(HardwareTestReport, id=report_id)
    serializer = HardwareTestReportSerializer(report)
    return Response(serializer.data)

# API: Create a new report
@api_view(['POST'])
def create_report(request):
    data = request.data
    

    # ✅ Create Main Report
    report = HardwareTestReport.objects.create(
        project_name=data.get('project_name', ''),
        test_date=data.get('test_date', None),
        tested_by=data.get('tested_by', '')
    )

    # ✅ Insert Test Environment
    environment_data = data.get('environment', {})
    if environment_data:
        TestEnvironment.objects.create(
            report=report,
            hardware_version=environment_data.get('hardware_version', ''),
            firmware_version=environment_data.get('firmware_version', ''),
            test_equipment_used=environment_data.get('test_equipment_used', ''),
            operating_conditions=environment_data.get('operating_conditions', '')
        )

    # ✅ Insert Multiple Test Cases
    test_cases_data = data.get('test_cases', [])
    if isinstance(test_cases_data, list):
        for test_case in test_cases_data:
            TestCase.objects.create(
                report=report,
                test_case_no=test_case.get('test_case_no', 1),
                test_description=test_case.get('test_description', ''),
                expected_outcome=test_case.get('expected_outcome', ''),
                actual_outcome=test_case.get('actual_outcome', ''),
                status=test_case.get('status', 'Pending')
            )

    # ✅ Insert Multiple Issues & Observations
    issues_data = data.get('issues', [])
    if isinstance(issues_data, list):
        for issue in issues_data:
            IssueObservation.objects.create(
                report=report,
                issue_description=issue.get('issue_description', ''),
                suggested_resolution=issue.get('suggested_resolution', '')
            )

    # ✅ Insert Conclusion (Check for empty data)
    conclusion_data = data.get('conclusion', [{}])
    if isinstance(conclusion_data, list) and len(conclusion_data) > 0:
        ConclusionRecommendation.objects.create(
            report=report,
            summary=conclusion_data[0].get('summary', ''),
            next_steps=conclusion_data[0].get('next_steps', ''),
            approved_by=conclusion_data[0].get('approved_by', ''),
            approval_date=conclusion_data[0].get('approval_date', None)
        )

    return Response({"message": "✅ Report created successfully"}, status=status.HTTP_201_CREATED)

@api_view(['PUT'])
def update_report(request, report_id):
    report = get_object_or_404(HardwareTestReport, id=report_id)
    
    # ✅ Update the main report details
    report.project_name = request.data.get('project_name', report.project_name)
    report.test_date = request.data.get('test_date', report.test_date)
    report.tested_by = request.data.get('tested_by', report.tested_by)
    report.save()

    # ✅ Update Test Environment (should be a single object, not a list)
    if 'environment' in request.data:
        env_data = request.data['environment']
        environment, created = TestEnvironment.objects.update_or_create(
            report=report,
            defaults={
                "hardware_version": env_data.get('hardware_version', ""),
                "firmware_version": env_data.get('firmware_version', ""),
                "test_equipment_used": env_data.get('test_equipment_used', ""),
                "operating_conditions": env_data.get('operating_conditions', "")
            }
        )

    # ✅ Update Test Cases (don't delete, update existing ones)
    if 'test_cases' in request.data:
        for test_case_data in request.data['test_cases']:
            TestCase.objects.update_or_create(
                report=report,
                test_case_no=test_case_data.get('test_case_no'),
                defaults={
                    "test_description": test_case_data.get('test_description', ""),
                    "expected_outcome": test_case_data.get('expected_outcome', ""),
                    "actual_outcome": test_case_data.get('actual_outcome', ""),
                    "status": test_case_data.get('status', "Pass")
                }
            )

    # ✅ Update Issues (update instead of deleting)
    if 'issues' in request.data:
        for issue_data in request.data['issues']:
            IssueObservation.objects.update_or_create(
                report=report,
                issue_description=issue_data.get('issue_description'),
                defaults={"suggested_resolution": issue_data.get('suggested_resolution', "")}
            )

    # ✅ Fix: Update Conclusion (don't delete, just update existing ones)
    if 'conclusion' in request.data:
        for conclusion_data in request.data['conclusion']:
            ConclusionRecommendation.objects.update_or_create(
                report=report,
                defaults={
                    "summary": conclusion_data.get('summary', ""),
                    "next_steps": conclusion_data.get('next_steps', ""),
                    "approved_by": conclusion_data.get('approved_by', ""),
                    "approval_date": conclusion_data.get('approval_date', None)
                }
            )

    return Response({"message": "Report updated successfully"}, status=status.HTTP_200_OK)

# API: Delete a report
@api_view(['DELETE'])
def delete_report(request, report_id):
    report = get_object_or_404(HardwareTestReport, id=report_id)

    # Delete related entries first
    report.environment.all().delete()
    report.test_cases.all().delete()
    report.issues.all().delete()
    report.conclusion.all().delete()

    # Now delete the main report
    report.delete()

    return Response({"message": "Report deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
#=================================================================Firmware=======================================================

from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import FirmwareTestReport
from .serializers import FirmwareTestReportSerializer

# ✅ Create a new firmware test report
@api_view(['POST'])
def create_firmware_test_report(request):
    serializer = FirmwareTestReportSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Firmware Test Report Created Successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ✅ Get all firmware test reports
@api_view(['GET'])
def get_all_firmware_test_reports(request):
    reports = FirmwareTestReport.objects.all()
    serializer = FirmwareTestReportSerializer(reports, many=True)
    return Response(serializer.data)

# ✅ Get a single firmware test report by ID
@api_view(['GET'])
def get_firmware_test_report_by_id(request, report_id):
    report = get_object_or_404(FirmwareTestReport, id=report_id)
    serializer = FirmwareTestReportSerializer(report)
    return Response(serializer.data)

# ✅ Update an existing firmware test report
@api_view(['PUT'])
def update_firmware_test_report(request, report_id):
    report = get_object_or_404(FirmwareTestReport, id=report_id)
    serializer = FirmwareTestReportSerializer(report, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Firmware Test Report Updated Successfully", "data": serializer.data}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ✅ Delete a firmware test report
@api_view(['DELETE'])
def delete_firmware_test_report(request, report_id):
    report = get_object_or_404(FirmwareTestReport, id=report_id)
    report.delete()
    return Response({"message": "Firmware Test Report Deleted Successfully"}, status=status.HTTP_204_NO_CONTENT)


#======================================================Firmware Driver Document=========================================


from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import FirmwareDriverDocument
from .serializers import FirmwareDriverDocumentSerializer

# ✅ Create a new firmware driver document
@api_view(['POST'])
def create_firmware_driver_document(request):
    serializer = FirmwareDriverDocumentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Firmware Driver Document Created Successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ✅ Get all firmware driver documents
@api_view(['GET'])
def get_all_firmware_driver_documents(request):
    documents = FirmwareDriverDocument.objects.all()
    serializer = FirmwareDriverDocumentSerializer(documents, many=True)
    return Response(serializer.data)

# ✅ Get a single firmware driver document by ID
@api_view(['GET'])
def get_firmware_driver_document_by_id(request, document_id):
    document = get_object_or_404(FirmwareDriverDocument, id=document_id)
    serializer = FirmwareDriverDocumentSerializer(document)
    return Response(serializer.data)

# ✅ Update an existing firmware driver document
@api_view(['PUT'])
def update_firmware_driver_document(request, document_id):
    document = get_object_or_404(FirmwareDriverDocument, id=document_id)
    serializer = FirmwareDriverDocumentSerializer(document, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Firmware Driver Document Updated Successfully", "data": serializer.data}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ✅ Delete a firmware driver document
@api_view(['DELETE'])
def delete_firmware_driver_document(request, document_id):
    document = get_object_or_404(FirmwareDriverDocument, id=document_id)
    document.delete()
    return Response({"message": "Firmware Driver Document Deleted Successfully"}, status=status.HTTP_204_NO_CONTENT)


#=============================================FirmwareLowLevelDesign=======================================================

from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import FirmwareLowLevelDesign
from .serializers import FirmwareLowLevelDesignSerializer

# ✅ Create a new firmware low-level design document
@api_view(['POST'])
def create_firmware_low_level_design(request):
    serializer = FirmwareLowLevelDesignSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Firmware Low-Level Design Created Successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ✅ Get all firmware low-level design documents
@api_view(['GET'])
def get_all_firmware_low_level_designs(request):
    documents = FirmwareLowLevelDesign.objects.all()
    serializer = FirmwareLowLevelDesignSerializer(documents, many=True)
    return Response(serializer.data)

# ✅ Get a single firmware low-level design document by ID
@api_view(['GET'])
def get_firmware_low_level_design_by_id(request, document_id):
    document = get_object_or_404(FirmwareLowLevelDesign, id=document_id)
    serializer = FirmwareLowLevelDesignSerializer(document)
    return Response(serializer.data)

# ✅ Update an existing firmware low-level design document
@api_view(['PUT'])
def update_firmware_low_level_design(request, document_id):
    document = get_object_or_404(FirmwareLowLevelDesign, id=document_id)
    serializer = FirmwareLowLevelDesignSerializer(document, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Firmware Low-Level Design Updated Successfully", "data": serializer.data}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ✅ Delete a firmware low-level design document
@api_view(['DELETE'])
def delete_firmware_low_level_design(request, document_id):
    document = get_object_or_404(FirmwareLowLevelDesign, id=document_id)
    document.delete()
    return Response({"message": "Firmware Low-Level Design Deleted Successfully"}, status=status.HTTP_204_NO_CONTENT)



#====================================================FirmwareProtocolDocument========================================

from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import FirmwareProtocolDocument
from .serializers import FirmwareProtocolDocumentSerializer

# ✅ Create a new firmware protocol document
@api_view(['POST'])
def create_firmware_protocol_document(request):
    serializer = FirmwareProtocolDocumentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Firmware Protocol Document Created Successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ✅ Get all firmware protocol documents
@api_view(['GET'])
def get_all_firmware_protocol_documents(request):
    documents = FirmwareProtocolDocument.objects.all()
    serializer = FirmwareProtocolDocumentSerializer(documents, many=True)
    return Response(serializer.data)

# ✅ Get a single firmware protocol document by ID
@api_view(['GET'])
def get_firmware_protocol_document_by_id(request, document_id):
    document = get_object_or_404(FirmwareProtocolDocument, id=document_id)
    serializer = FirmwareProtocolDocumentSerializer(document)
    return Response(serializer.data)

# ✅ Update an existing firmware protocol document
@api_view(['PUT'])
def update_firmware_protocol_document(request, document_id):
    document = get_object_or_404(FirmwareProtocolDocument, id=document_id)
    serializer = FirmwareProtocolDocumentSerializer(document, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Firmware Protocol Document Updated Successfully", "data": serializer.data}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ✅ Delete a firmware protocol document
@api_view(['DELETE'])
def delete_firmware_protocol_document(request, document_id):
    document = get_object_or_404(FirmwareProtocolDocument, id=document_id)
    document.delete()
    return Response({"message": "Firmware Protocol Document Deleted Successfully"}, status=status.HTTP_204_NO_CONTENT)


# ===============================RS485 Modbus Protocol Document===================================================

from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import RS485ModbusProtocolDocument
from .serializers import RS485ModbusProtocolDocumentSerializer

# ✅ Create a new RS485 Modbus Protocol document
@api_view(['POST'])
def create_rs485_modbus_document(request):
    serializer = RS485ModbusProtocolDocumentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "RS485 Modbus Protocol Document Created Successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ✅ Get all RS485 Modbus Protocol documents
@api_view(['GET'])
def get_all_rs485_modbus_documents(request):
    documents = RS485ModbusProtocolDocument.objects.all()
    serializer = RS485ModbusProtocolDocumentSerializer(documents, many=True)
    return Response(serializer.data)

# ✅ Get a single RS485 Modbus Protocol document by ID
@api_view(['GET'])
def get_rs485_modbus_document_by_id(request, document_id):
    document = get_object_or_404(RS485ModbusProtocolDocument, id=document_id)
    serializer = RS485ModbusProtocolDocumentSerializer(document)
    return Response(serializer.data)

# ✅ Update an existing RS485 Modbus Protocol document
@api_view(['PUT'])
def update_rs485_modbus_document(request, document_id):
    document = get_object_or_404(RS485ModbusProtocolDocument, id=document_id)
    serializer = RS485ModbusProtocolDocumentSerializer(document, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "RS485 Modbus Protocol Document Updated Successfully", "data": serializer.data}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ✅ Delete a RS485 Modbus Protocol document
@api_view(['DELETE'])
def delete_rs485_modbus_document(request, document_id):
    document = get_object_or_404(RS485ModbusProtocolDocument, id=document_id)
    document.delete()
    return Response({"message": "RS485 Modbus Protocol Document Deleted Successfully"}, status=status.HTTP_204_NO_CONTENT)


#==================================== High-Level Design Document details ======================================

from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import HighLevelDesignDocument
from .serializers import HighLevelDesignDocumentSerializer

# ✅ Create a new High-Level Design document
@api_view(['POST'])
def create_high_level_design(request):
    serializer = HighLevelDesignDocumentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "High-Level Design Document Created Successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ✅ Get all High-Level Design documents
@api_view(['GET'])
def get_all_high_level_designs(request):
    documents = HighLevelDesignDocument.objects.all()
    serializer = HighLevelDesignDocumentSerializer(documents, many=True)
    return Response(serializer.data)

# ✅ Get a single High-Level Design document by ID
@api_view(['GET'])
def get_high_level_design_by_id(request, document_id):
    document = get_object_or_404(HighLevelDesignDocument, id=document_id)
    serializer = HighLevelDesignDocumentSerializer(document)
    return Response(serializer.data)

# ✅ Update an existing High-Level Design document
@api_view(['PUT'])
def update_high_level_design(request, document_id):
    document = get_object_or_404(HighLevelDesignDocument, id=document_id)
    serializer = HighLevelDesignDocumentSerializer(document, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "High-Level Design Document Updated Successfully", "data": serializer.data}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ✅ Delete a High-Level Design document
@api_view(['DELETE'])
def delete_high_level_design(request, document_id):
    document = get_object_or_404(HighLevelDesignDocument, id=document_id)
    document.delete()
    return Response({"message": "High-Level Design Document Deleted Successfully"}, status=status.HTTP_204_NO_CONTENT)


#===================================== Software High-Level Design Document details =================================

from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import SoftwareHLDDocument
from .serializers import SoftwareHLDDocumentSerializer

# ✅ Create a new Software HLD document
@api_view(['POST'])
def create_software_hld(request):
    serializer = SoftwareHLDDocumentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Software HLD Document Created Successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ✅ Get all Software HLD documents
@api_view(['GET'])
def get_all_software_hld(request):
    documents = SoftwareHLDDocument.objects.all()
    serializer = SoftwareHLDDocumentSerializer(documents, many=True)
    return Response(serializer.data)

# ✅ Get a single Software HLD document by ID
@api_view(['GET'])
def get_software_hld_by_id(request, document_id):
    document = get_object_or_404(SoftwareHLDDocument, id=document_id)
    serializer = SoftwareHLDDocumentSerializer(document)
    return Response(serializer.data)

# ✅ Update an existing Software HLD document
@api_view(['PUT'])
def update_software_hld(request, document_id):
    document = get_object_or_404(SoftwareHLDDocument, id=document_id)
    serializer = SoftwareHLDDocumentSerializer(document, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Software HLD Document Updated Successfully", "data": serializer.data}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ✅ Delete a Software HLD document
@api_view(['DELETE'])
def delete_software_hld(request, document_id):
    document = get_object_or_404(SoftwareHLDDocument, id=document_id)
    document.delete()
    return Response({"message": "Software HLD Document Deleted Successfully"}, status=status.HTTP_204_NO_CONTENT)


#===================================== Software Low-Level Design (LLD) Document =================================

from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import SoftwareLLDDocument
from .serializers import SoftwareLLDDocumentSerializer

# ✅ Create a new Software LLD document
@api_view(['POST'])
def create_software_lld(request):
    serializer = SoftwareLLDDocumentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Software LLD Document Created Successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ✅ Get all Software LLD documents
@api_view(['GET'])
def get_all_software_lld(request):
    documents = SoftwareLLDDocument.objects.all()
    serializer = SoftwareLLDDocumentSerializer(documents, many=True)
    return Response(serializer.data)

# ✅ Get a single Software LLD document by ID
@api_view(['GET'])
def get_software_lld_by_id(request, document_id):
    document = get_object_or_404(SoftwareLLDDocument, id=document_id)
    serializer = SoftwareLLDDocumentSerializer(document)
    return Response(serializer.data)

# ✅ Update an existing Software LLD document
@api_view(['PUT'])
def update_software_lld(request, document_id):
    document = get_object_or_404(SoftwareLLDDocument, id=document_id)
    serializer = SoftwareLLDDocumentSerializer(document, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Software LLD Document Updated Successfully", "data": serializer.data}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ✅ Delete a Software LLD document
@api_view(['DELETE'])
def delete_software_lld(request, document_id):
    document = get_object_or_404(SoftwareLLDDocument, id=document_id)
    document.delete()
    return Response({"message": "Software LLD Document Deleted Successfully"}, status=status.HTTP_204_NO_CONTENT)


#============================================= Software Requirements Specification (SRS) Document=======================

from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import SoftwareSRS
from .serializers import SoftwareSRSSerializer

# ✅ Create a new SRS document
@api_view(['POST'])
def create_srs(request):
    serializer = SoftwareSRSSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "SRS Document Created Successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ✅ Get all SRS documents
@api_view(['GET'])
def get_all_srs(request):
    documents = SoftwareSRS.objects.all()
    serializer = SoftwareSRSSerializer(documents, many=True)
    return Response(serializer.data)

# ✅ Get a single SRS document by ID
@api_view(['GET'])
def get_srs_by_id(request, document_id):
    document = get_object_or_404(SoftwareSRS, id=document_id)
    serializer = SoftwareSRSSerializer(document)
    return Response(serializer.data)

# ✅ Update an existing SRS document
@api_view(['PUT'])
def update_srs(request, document_id):
    document = get_object_or_404(SoftwareSRS, id=document_id)
    serializer = SoftwareSRSSerializer(document, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "SRS Document Updated Successfully", "data": serializer.data}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ✅ Delete an SRS document
@api_view(['DELETE'])
def delete_srs(request, document_id):
    document = get_object_or_404(SoftwareSRS, id=document_id)
    document.delete()
    return Response({"message": "SRS Document Deleted Successfully"}, status=status.HTTP_204_NO_CONTENT)

#==============================Software Test Specification Document details=======================================
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import SoftwareTestSpecification
from .serializers import SoftwareTestSpecificationSerializer

# ✅ Create a new Software Test Specification document
@api_view(['POST'])
def create_test_specification(request):
    serializer = SoftwareTestSpecificationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Test Specification Document Created Successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ✅ Get all Test Specification documents
@api_view(['GET'])
def get_all_test_specifications(request):
    documents = SoftwareTestSpecification.objects.all()
    serializer = SoftwareTestSpecificationSerializer(documents, many=True)
    return Response(serializer.data)

# ✅ Get a single Test Specification document by ID
@api_view(['GET'])
def get_test_specification_by_id(request, document_id):
    document = get_object_or_404(SoftwareTestSpecification, id=document_id)
    serializer = SoftwareTestSpecificationSerializer(document)
    return Response(serializer.data)

# ✅ Update an existing Test Specification document
@api_view(['PUT'])
def update_test_specification(request, document_id):
    document = get_object_or_404(SoftwareTestSpecification, id=document_id)
    serializer = SoftwareTestSpecificationSerializer(document, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Test Specification Document Updated Successfully", "data": serializer.data}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ✅ Delete a Test Specification document
@api_view(['DELETE'])
def delete_test_specification(request, document_id):
    document = get_object_or_404(SoftwareTestSpecification, id=document_id)
    document.delete()
    return Response({"message": "Test Specification Document Deleted Successfully"}, status=status.HTTP_204_NO_CONTENT)



#================================================ Hardware Low-Level Design (LLD) Document details.==========================
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import HardwareLLD
from .serializers import HardwareLLDSerializer

@api_view(['POST'])
def create_hardware_lld(request):
    serializer = HardwareLLDSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Hardware LLD Document Created Successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_all_hardware_lld(request):
    documents = HardwareLLD.objects.all()
    serializer = HardwareLLDSerializer(documents, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_hardware_lld_by_id(request, document_id):
    document = get_object_or_404(HardwareLLD, id=document_id)
    serializer = HardwareLLDSerializer(document)
    return Response(serializer.data)

@api_view(['PUT'])
def update_hardware_lld(request, document_id):
    document = get_object_or_404(HardwareLLD, id=document_id)
    serializer = HardwareLLDSerializer(document, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Hardware LLD Document Updated Successfully", "data": serializer.data}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_hardware_lld(request, document_id):
    document = get_object_or_404(HardwareLLD, id=document_id)
    document.delete()
    return Response({"message": "Hardware LLD Document Deleted Successfully"}, status=status.HTTP_204_NO_CONTENT)



#========================================Low-Level Design (LLD) Document details.===================================
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import LowLevelDesignFunctional
from .serializers import LowLevelDesignFunctionalSerializer

@api_view(['POST'])
def create_lld(request):
    serializer = LowLevelDesignFunctionalSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "LLD Functional Document Created Successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_all_lld(request):
    documents = LowLevelDesignFunctional.objects.all()
    serializer = LowLevelDesignFunctionalSerializer(documents, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_lld_by_id(request, document_id):
    document = get_object_or_404(LowLevelDesignFunctional, id=document_id)
    serializer = LowLevelDesignFunctionalSerializer(document)
    return Response(serializer.data)

@api_view(['PUT'])
def update_lld(request, document_id):
    document = get_object_or_404(LowLevelDesignFunctional, id=document_id)
    serializer = LowLevelDesignFunctionalSerializer(document, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "LLD Functional Document Updated Successfully", "data": serializer.data}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_lld(request, document_id):
    document = get_object_or_404(LowLevelDesignFunctional, id=document_id)
    document.delete()
    return Response({"message": "LLD Functional Document Deleted Successfully"}, status=status.HTTP_204_NO_CONTENT)



# ===========================================Milestone Schedule Chart================================================


from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import MilestoneSchedule
from .serializers import MilestoneScheduleSerializer

@api_view(['POST'])
def create_schedule(request):
    serializer = MilestoneScheduleSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Milestone Schedule Created Successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_all_schedules(request):
    schedules = MilestoneSchedule.objects.all()
    serializer = MilestoneScheduleSerializer(schedules, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_schedule_by_id(request, schedule_id):
    schedule = get_object_or_404(MilestoneSchedule, id=schedule_id)
    serializer = MilestoneScheduleSerializer(schedule)
    return Response(serializer.data)

@api_view(['PUT'])
def update_schedule(request, schedule_id):
    schedule = get_object_or_404(MilestoneSchedule, id=schedule_id)
    serializer = MilestoneScheduleSerializer(schedule, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Milestone Schedule Updated Successfully", "data": serializer.data}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_schedule(request, schedule_id):
    schedule = get_object_or_404(MilestoneSchedule, id=schedule_id)
    schedule.delete()
    return Response({"message": "Milestone Schedule Deleted Successfully"}, status=status.HTTP_204_NO_CONTENT)


#==================================   User Acceptance Test (UAT) Document ========================


from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import UATDocument
from .serializers import UATDocumentSerializer

@api_view(['POST'])
def create_uat_document(request):
    serializer = UATDocumentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "UAT Document Created Successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_all_uat_documents(request):
    documents = UATDocument.objects.all()
    serializer = UATDocumentSerializer(documents, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_uat_document_by_id(request, document_id):
    document = get_object_or_404(UATDocument, id=document_id)
    serializer = UATDocumentSerializer(document)
    return Response(serializer.data)

@api_view(['PUT'])
def update_uat_document(request, document_id):
    document = get_object_or_404(UATDocument, id=document_id)
    serializer = UATDocumentSerializer(document, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "UAT Document Updated Successfully", "data": serializer.data}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_uat_document(request, document_id):
    document = get_object_or_404(UATDocument, id=document_id)
    document.delete()
    return Response({"message": "UAT Document Deleted Successfully"}, status=status.HTTP_204_NO_CONTENT)

