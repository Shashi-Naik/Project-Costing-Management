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
