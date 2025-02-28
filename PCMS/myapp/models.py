
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