from django.urls import path
from . import views

urlpatterns = [
    # Serve HTML Pages
    path('reports/form/', views.report_form, name='report_form'),
    path('reports/view/', views.report_list, name='report_list'),
    path('reports/edit/<int:report_id>/', views.edit_report, name='edit_report'),

    # REST API Endpoints
    path('reports/', views.get_reports, name='get_reports'),
    path('reports/<int:report_id>/', views.get_report_by_id, name='get_report_by_id'),
    path('reports/create/', views.create_report, name='create_report'),
    path('reports/<int:report_id>/update/', views.update_report, name='update_report'),
    path('reports/<int:report_id>/delete/', views.delete_report, name='delete_report'),
    #================================Firmware========================================
    
    path('firmware_test/create/', views.create_firmware_test_report, name='create_firmware_test_report'),
    path('firmware_test/', views.get_all_firmware_test_reports, name='get_all_firmware_test_reports'),
    path('firmware_test/<int:report_id>/', views.get_firmware_test_report_by_id, name='get_firmware_test_report_by_id'),
    path('firmware_test/<int:report_id>/update/', views.update_firmware_test_report, name='update_firmware_test_report'),
    path('firmware_test/<int:report_id>/delete/', views.delete_firmware_test_report, name='delete_firmware_test_report'),
    
    #==============================Firmware Driver Document=========================================

    path('firmware_driver/create/', views.create_firmware_driver_document, name='create_firmware_driver_document'),
    path('firmware_driver/', views.get_all_firmware_driver_documents, name='get_all_firmware_driver_documents'),
    path('firmware_driver/<int:document_id>/', views.get_firmware_driver_document_by_id, name='get_firmware_driver_document_by_id'),
    path('firmware_driver/<int:document_id>/update/', views.update_firmware_driver_document, name='update_firmware_driver_document'),
    path('firmware_driver/<int:document_id>/delete/', views.delete_firmware_driver_document, name='delete_firmware_driver_document'),
    
    #=============================================FirmwareLowLevelDesign=======================================================

    path('firmware_low_level/create/', views.create_firmware_low_level_design, name='create_firmware_low_level_design'),
    path('firmware_low_level/', views.get_all_firmware_low_level_designs, name='get_all_firmware_low_level_designs'),
    path('firmware_low_level/<int:document_id>/', views.get_firmware_low_level_design_by_id, name='get_firmware_low_level_design_by_id'),
    path('firmware_low_level/<int:document_id>/update/', views.update_firmware_low_level_design, name='update_firmware_low_level_design'),
    path('firmware_low_level/<int:document_id>/delete/', views.delete_firmware_low_level_design, name='delete_firmware_low_level_design'),

    #====================================================FirmwareProtocolDocument========================================

    path('firmware_protocol/create/', views.create_firmware_protocol_document, name='create_firmware_protocol_document'),
    path('firmware_protocol/', views.get_all_firmware_protocol_documents, name='get_all_firmware_protocol_documents'),
    path('firmware_protocol/<int:document_id>/', views.get_firmware_protocol_document_by_id, name='get_firmware_protocol_document_by_id'),
    path('firmware_protocol/<int:document_id>/update/', views.update_firmware_protocol_document, name='update_firmware_protocol_document'),
    path('firmware_protocol/<int:document_id>/delete/', views.delete_firmware_protocol_document, name='delete_firmware_protocol_document'),
    
    # ===============================RS485 Modbus Protocol Document===================================================

    path('rs485_modbus/create/', views.create_rs485_modbus_document, name='create_rs485_modbus_document'),
    path('rs485_modbus/', views.get_all_rs485_modbus_documents, name='get_all_rs485_modbus_documents'),
    path('rs485_modbus/<int:document_id>/', views.get_rs485_modbus_document_by_id, name='get_rs485_modbus_document_by_id'),
    path('rs485_modbus/<int:document_id>/update/', views.update_rs485_modbus_document, name='update_rs485_modbus_document'),
    path('rs485_modbus/<int:document_id>/delete/', views.delete_rs485_modbus_document, name='delete_rs485_modbus_document'),

    #==================================== High-Level Design Document details ======================================

    path('high_level_design/create/', views.create_high_level_design, name='create_high_level_design'),
    path('high_level_design/', views.get_all_high_level_designs, name='get_all_high_level_designs'),
    path('high_level_design/<int:document_id>/', views.get_high_level_design_by_id, name='get_high_level_design_by_id'),
    path('high_level_design/<int:document_id>/update/', views.update_high_level_design, name='update_high_level_design'),
    path('high_level_design/<int:document_id>/delete/', views.delete_high_level_design, name='delete_high_level_design'),
    
    #===================================== Software High-Level Design Document details =================================
    
    path('software_hld/create/', views.create_software_hld, name='create_software_hld'),
    path('software_hld/', views.get_all_software_hld, name='get_all_software_hld'),
    path('software_hld/<int:document_id>/', views.get_software_hld_by_id, name='get_software_hld_by_id'),
    path('software_hld/<int:document_id>/update/', views.update_software_hld, name='update_software_hld'),
    path('software_hld/<int:document_id>/delete/', views.delete_software_hld, name='delete_software_hld'),
    
    #===================================== Software Low-Level Design (LLD) Document =================================
    
    path('software_lld/create/', views.create_software_lld, name='create_software_lld'),
    path('software_lld/', views.get_all_software_lld, name='get_all_software_lld'),
    path('software_lld/<int:document_id>/', views.get_software_lld_by_id, name='get_software_lld_by_id'),
    path('software_lld/<int:document_id>/update/', views.update_software_lld, name='update_software_lld'),
    path('software_lld/<int:document_id>/delete/', views.delete_software_lld, name='delete_software_lld'),
    
    #============================================= Software Requirements Specification (SRS) Document=======================

    path('srs/create/', views.create_srs, name='create_srs'),
    path('srs/', views.get_all_srs, name='get_all_srs'),
    path('srs/<int:document_id>/', views.get_srs_by_id, name='get_srs_by_id'),
    path('srs/<int:document_id>/update/', views.update_srs, name='update_srs'),
    path('srs/<int:document_id>/delete/', views.delete_srs, name='delete_srs'),
    
    #==============================Software Test Specification Document details=======================================



    path('test_specification/create/', views.create_test_specification, name='create_test_specification'),
    path('test_specification/', views.get_all_test_specifications, name='get_all_test_specifications'),
    path('test_specification/<int:document_id>/', views.get_test_specification_by_id, name='get_test_specification_by_id'),
    path('test_specification/<int:document_id>/update/', views.update_test_specification, name='update_test_specification'),
    path('test_specification/<int:document_id>/delete/', views.delete_test_specification, name='delete_test_specification'),
    
    
#================================================ Hardware Low-Level Design (LLD) Document details.==========================
    
    path('hardware_lld/create/', views.create_hardware_lld, name='create_hardware_lld'),
    path('hardware_lld/', views.get_all_hardware_lld, name='get_all_hardware_lld'),
    path('hardware_lld/<int:document_id>/', views.get_hardware_lld_by_id, name='get_hardware_lld_by_id'),
    path('hardware_lld/<int:document_id>/update/', views.update_hardware_lld, name='update_hardware_lld'),
    path('hardware_lld/<int:document_id>/delete/', views.delete_hardware_lld, name='delete_hardware_lld'),
    
#========================================Low-Level Design (LLD) Document details.===================================
    
    path('lld/create/', views.create_lld, name='create_lld'),
    path('lld/', views.get_all_lld, name='get_all_lld'),
    path('lld/<int:document_id>/', views.get_lld_by_id, name='get_lld_by_id'),
    path('lld/<int:document_id>/update/', views.update_lld, name='update_lld'),
    path('lld/<int:document_id>/delete/', views.delete_lld, name='delete_lld'),
    
# ===========================================Milestone Schedule Chart================================================
    
    path('schedule/create/', views.create_schedule, name='create_schedule'),
    path('schedule/', views.get_all_schedules, name='get_all_schedules'),
    path('schedule/<int:schedule_id>/', views.get_schedule_by_id, name='get_schedule_by_id'),
    path('schedule/<int:schedule_id>/update/', views.update_schedule, name='update_schedule'),
    path('schedule/<int:schedule_id>/delete/', views.delete_schedule, name='delete_schedule'),
    
#==================================   User Acceptance Test (UAT) Document ========================



    path('uat/create/', views.create_uat_document, name='create_uat_document'),
    path('uat/', views.get_all_uat_documents, name='get_all_uat_documents'),
    path('uat/<int:document_id>/', views.get_uat_document_by_id, name='get_uat_document_by_id'),
    path('uat/<int:document_id>/update/', views.update_uat_document, name='update_uat_document'),
    path('uat/<int:document_id>/delete/', views.delete_uat_document, name='delete_uat_document'),
    
    
]
