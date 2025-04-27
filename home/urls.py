from  django.urls import include,path
from . import views
from .views import login_view, logout_view
from .views import admin_dashboard,  approver_dashboard


urlpatterns = [
    # path('', views.index, name='home'),
    path('', login_view, name='login'),
    path('class/', views.dsc_class, name='class'),
    path('class/edit/<int:class_id>/', views.edit_class, name='edit_class'),
    path('class/delete/<int:class_id>/', views.delete_class, name='delete_class'),
    path('platform/', views.platform, name='platform'),
    path('platform/edit/<int:platform_id>/', views.edit_platform, name='edit_platform'),
    path('platform/delete/<int:platform_id>/', views.delete_platform, name='delete_platform'),
    path('issuingauth/', views.issuingauth, name='issuingauth'),
    path('issuingauth/edit/<int:auth_id>/', views.edit_issuingauth, name='edit_issuingauth'),
    path('issuingauth/delete/<int:auth_id>/', views.delete_issuingauth, name='delete_issuingauth'),
    path('entity/', views.entity, name='entity'),
    path('entity/edit/<int:entity_id>/', views.edit_entity, name='edit_entity'),
    path('entity/delete/<int:entity_id>/', views.delete_entity, name='delete_entity'),
    path('licenseperiod/', views.licenseperiod, name='licenseperiod'),
    path('licenseperiod/edit/<int:license_id>/', views.edit_licenseperiod, name='edit_licenseperiod'),
    path('licenseperiod/delete/<int:license_id>/', views.delete_licenseperiod, name='delete_licenseperiod'),
    path('forms/', views.forms, name='forms'),
    path('forms/edit/<int:form_id>/', views.edit_forms, name='edit_forms'),
    path('forms/delete/<int:form_id>/', views.delete_forms, name='delete_forms'),
    path('type/', views.type, name='type'),
    path('type/edit/<int:type_id>/', views.edit_type, name='edit_type'),
    path('type/delete/<int:type_id>/', views.delete_type, name='delete_type'),
    path('shelf/', views.shelf, name='shelf'),
    path('shelf/edit/<int:shelf_id>/', views.edit_shelf, name='edit_shelf'),
    path('shelf/delete/<int:shelf_id>/', views.delete_shelf, name='delete_shelf'),
    
    # path('dsc_display/<int:dsc_id>/', views.dsc_display, name='dsc_display'),
    # path('search_dsc/', views.search_dsc, name='search_dsc'),
    # path('dsc_display/', views.dsc_display, name='dsc_display'),


    path('renewal/', views.renewal, name='renewal'),
    path('additional-details/', views.additional_details, name='additional_details'),



    # path('inout/', views.inout, name='inout'),
    
    # path('newentry/', views.newentry, name='newentry'),
    path('internal_newentry/', views.internal_newentry, name='internal_newentry'),
    path('external_newentry/', views.external_newentry, name='external_newentry'),
    # path('docs/', views.docs, name='docs'),

    path('usage_logs/', views.usage_logs, name='usage_logs'),
    path('delete_usage_log/<int:log_id>/', views.delete_usage_log, name='delete_usage_log'),

    # path('login/', login_view, name='login'),
    # Add other URL patterns here

    path('search/', views.search_dsc, name='search_dsc'),
    path('dsc/<str:dsc_number>/', views.dsc_display, name='dsc_display'),
 
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),

    




    path("mark-not-renewing/<str:dsc_number>/", views.mark_not_renewing, name="mark_not_renewing"),
    path("mark-pending-renewal/<str:dsc_number>/", views.mark_pending_renewal, name="mark_pending_renewal"),

    path('map-dsc-entity/', views.map_dsc_entity, name='map_dsc_entity'),
    path('delete-mapping/<int:mapping_id>/', views.delete_mapping, name='delete_mapping'),  # ✅ Add this line



    path('manage-users/', views.manage_users, name='manage_users'),
    path('add-user/', views.add_user, name='add_user'),
    path('edit-user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),

    path('manage-extra-fields/', views.manage_extra_fields, name='manage_extra_fields'),
    path('backup/', views.backup_db, name='backup_db'),
    path('restore/', views.restore_db, name='restore_db'),

    path('export-excel/', views.export_all_models_excel, name='export_all_models_excel'),
####################################################General#user##############################################

    # path('user_renewal/', views.user_renewal, name='user_renewal'),
    # path('user_search_dsc/', views.user_search_dsc, name='user_search_dsc'),
    # path('user_dsc_display/<str:dsc_number>/', views.user_dsc_display, name='user_dsc_display'),

    
    # path('user_map_dsc_entity/', views.user_map_dsc_entity, name='user_map_dsc_entity'),
    # path('user_delete_mapping/<int:mapping_id>/', views.user_delete_mapping, name='user_delete_mapping'),
    # path('user_newentry/', views.user_newentry, name='user_newentry'),
    # path('user_inout/', views.user_inout, name='user_inout'),
    



    path("initiate-dsc/", views.initiate_dsc, name="initiate_dsc"),

    path("delivery/", views.delivery_collection, name="delivery_collection"),

    path('initiation-requests/', views.admin_initiation_requests, name='admin_initiation_requests'),
    path('request-details/<int:in_out_id>/', views.admin_request_details, name='admin_request_details'),

    path('dsc-list/', views.dsc_list, name='dsc_list'),
    path('export-dsc/<str:format>/', views.export_dsc_list, name='export_dsc_list'),

    path('manage_extra_fields/', views.ExtraFieldListView.as_view(), name='manage_extra_fields'),
    path('extra_field/add/', views.ExtraFieldCreateView.as_view(), name='extra_field_create'),
    path('extra_field/<int:pk>/edit/', views.ExtraFieldUpdateView.as_view(), name='extra_field_update'),
    path('extra_field/<int:pk>/delete/', views.ExtraFieldDeleteView.as_view(), name='extra_field_delete'),

    # path('admin/email-templates/', views.email_templates, name='email_templates'),
    # path('admin/email-templates/edit/<str:template_type>/', views.edit_template, name='edit_template'),
    # path('admin/send-notifications/<str:notification_type>/', views.send_manual_notifications, name='send_manual_notifications'),
    # path('admin/send-notificationss/<str:notification_type>/', views.send_notifications, name='send_notifications'),

    path('email-templates/', views.email_templates, name='email_templates'),
    path('email-templates/edit/<str:template_type>/', views.edit_template, name='edit_template'),
    path('send-notifications/<str:notification_type>/', views.send_notifications, name='send_notifications'),

    path('api/dsc-list/', views.api_dsc_list, name='api_dsc_list'),
################################################### General user ##############################################

    path('general-user-dashboard/', views.general_user_dashboard, name='general_user_dashboard'),
    path("general_user_mark_not_renewing/<str:dsc_number>/", views.general_user_mark_not_renewing, name="general_user_mark_not_renewing"),
    path("general_user_mark_pending_renewal/<str:dsc_number>/", views.general_user_mark_pending_renewal, name="general_user_mark_pending_renewal"),

    path('general_user_renewal/', views.general_user_renewal, name='general_user_renewal'),

    path('general_user_search_dsc/', views.general_user_search_dsc, name='general_user_search_dsc'),
    path('general_user_dsc_display/<str:dsc_number>/', views.general_user_dsc_display, name='general_user_dsc_display'),

    path('general_user_map_dsc_entity/', views.general_user_map_dsc_entity, name='general_user_map_dsc_entity'),
    path('general_user_delete_mapping/<int:mapping_id>/', views.general_user_delete_mapping, name='general_user_delete_mapping'),  # ✅ Add this line

    path('general_user_internal_newentry/', views.general_user_internal_newentry, name='general_user_internal_newentry'),
    path('general_user_external_newentry/', views.general_user_external_newentry, name='general_user_external_newentry'),


    path("general_user_initiate_dsc/", views.general_user_initiate_dsc, name="general_user_initiate_dsc"),
    path("general_user_delivery_collection/", views.general_user_delivery_collection, name="general_user_delivery_collection"),
    path('general_user_initiation_requests/', views.general_user_initiation_requests, name='general_user_initiation_requests'),
    path('general_user_request_details/<int:in_out_id>/', views.general_user_request_details, name='general_user_request_details'),

    path('general_user_usage_logs/', views.general_user_usage_logs, name='general_user_usage_logs'),
    path('general_user_delete_usage_log/<int:log_id>/', views.general_user_delete_usage_log, name='general_user_delete_usage_log'),

    path('general_user_additional_details/', views.general_user_additional_details, name='general_user_additional_details'),



################################################### Approver #######################################################

    path('approver-dashboard/', approver_dashboard, name='approver_dashboard'),
    path('approval-history/', views.approval_history, name='approval_history'),
    path('approve-usage-log/<int:log_id>/', views.approve_usage_log, name='approve_usage_log'),
    path('reject-usage-log/<int:log_id>/', views.reject_usage_log, name='reject_usage_log'),

]