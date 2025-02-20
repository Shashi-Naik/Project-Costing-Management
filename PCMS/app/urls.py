from django.urls import path
from . import views
from .views import bulk_update_view, tblProject_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path('', views.LoginPage, name = 'login'),
    path('logout/', views.LoginPage, name = 'logout'),
    
    
    path('bulk_update/', bulk_update_view, name='bulk_update_view'),
    path('Project/', tblProject_view, name='tblProject'),
    path('part-number/', views.part_number_view, name='tblPartNumber'),
    path('Vendordetails/', views.Vendordetails, name='Vendordetails'),
    #--------------------------------------------------
    path('CreateVendor/', views.CreateVendor_view, name='CreateVendor'),
    path('CreateCustomer/', views.CreateCustomer_view, name='CreateCustomer'),
    path('international_vendor/', views.international_customer_view, name='international_customer'),
    path('international_customer/', views.international_customer_2, name='international_customer_2'),
    
    path('CreateProject/', views.CreateProject_view, name='CreateProject'),
    path('UploadInvoicefromVendor/', views.UploadInvoicefromVendor_view, name='UploadInvoicefromVendor'),
    path('CreateInvoiceBasedPartNumber/', views.CreateInvoiceBasedPartNumber_view, name='CreateInvoiceBasedPartNumber'),
    path('CreatePurchaseBasedCosting/', views.CreatePurchaseBasedCosting_view, name='CreatePurchaseBasedCosting'),
    path('ReadPurchaseBasedCosting/', views.ReadPurchaseBasedCosting_view, name='ReadPurchaseBasedCosting'),
    
    path('SchArtifactUpload/', views.SchArtifactUpload_view, name='SchArtifactUpload'),
    path('engg_bom_upload/', views.engg_bom_upload_view, name='engg_bom_upload'),
    path('pcbartifactupload/', views.pcbartifactupload_view, name='pcbartifactupload_view'),
    path('PCBOrderDetailsUpload/', views.PCBOrderDetailsUpload_view, name='PCBOrderDetailsUpload'),
    path('mechanical_drawing/', views.MechanicalDrawingUpload_view, name='MechanicalDrawingUpload'),
    path('MechBOMUpload/', views.MechBOMUpload_view, name='MechBOMUpload'),
    
    
    path('costing/', views.project_dropdown_view, name='select_project'),
    path('qutation/', views.qutation, name='qutation'),
    
    path('Delivarychalan/', views.Delivarychalan, name='Delivarychalan'),
    path('gstr2b/', views.bulk_insert_gstr2b, name='gstr2b'),
    
    path('tree/', views.create_project_tree, name='create_project_tree'),
    path('create_mech_project/', views.create_mech_project, name='create_mech_project'),
    path('mechProject/', views.mechProject, name='mechProject'),
    path('upload_to_folder/', views.upload_to_folder, name='upload_to_folder'),
    path('PCBProject/', views.pcbProject, name='PCBProject'),
    path('upload_to_folder_pcb/', views.upload_to_folder_pcb, name='upload_to_folder_pcb'),
    path('sch/', views.SCHProject_view, name='sch'),
    path('upload_to_folder_sch/', views.upload_to_folder_sch, name='upload_to_folder_sch'),
    
    
    path('VendorStores/', views.CreateVendorStoresInward_views, name='CreateVendorStoresInward'),
    path('CustomerStore/', views.CreateCustomerStoresInward_views, name='CreateCustomerStoresInward'),
    path('OtherStore/', views.CreateOthersStoresInward_views, name='CreateOthersStoresInward'),
    path('Productionstore/', views.CreateStoresOutwardtoProduction_views, name='CreateStoresOutwardtoProduction'),
    path('StoreSales/', views.CreateStoresOutwardtoSales_views, name='CreateStoresOutwardtoSales'),
    path('StoreRND/', views.CreateStoresOutwardtoRnD_views, name='CreateStoresOutwardtoRnD'),
    path('StoreRepair/', views.CreateStoresOutwardtoRepairs_views, name='CreateStoresOutwardtoRepairs'),
    path('racks/', views.racks_view, name='racks'), 
    path('bins/', views.bins_view, name='bins'),
    path('RacksandBinsMapping/', views.RacksandBinsMapping_view, name='RacksandBinsMapping'), 
    
    path('create/', views.create_report, name='create_report'),
    path('reports/', views.list_reports, name='list_reports'),
    path('report/<int:report_id>/', views.report_details, name='report_details'),
    path('edit/<int:report_id>/', views.edit_report, name='edit_report'),
    path('hwReport/', views.Report, name='hwReport'),
    
  
   
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



