import csv

from django.contrib import admin
from django.http import HttpResponse

from vendor.models import VendorPlanner, VendorMeetingRegister
from delegate.models import Delegate, DelegateMeetingRegister

from import_export.admin import ImportExportModelAdmin
from import_export.resources import ModelResource
from django.core.exceptions import ObjectDoesNotExist

import openpyxl
from openpyxl import Workbook




class VendorPlannerResource(ModelResource):
    class Meta:
        model = VendorPlanner
        fields = ('id', 'company_name', 'country', 'first_name', 'last_name', 'job_title', 'company_type',
                  'website', 'asia_pacific', 'middle_east_africa', 'europe', 'north_america', 'canada',
                  'south_central_america', 'caribbean', 'budget_for_events', 'weddings_per_year')

# Register your models here.
@admin.action(description='Mark selected Vendor Planners as active')
def mark_active(modeladmin, request, queryset):
    queryset.update(is_active=True)


@admin.action(description='Mark selected Vendor Planners as inactive')
def mark_inactive(modeladmin, request, queryset):
    queryset.update(is_active=False)


class VendorPlannerAdmin(ImportExportModelAdmin):
    resource_class = VendorPlannerResource
    list_display = ('company_name',  'is_active')
    list_filter = ('is_active',)
    search_fields = ('company_name',)

    fieldsets = (
        ("Base Info", {
            'fields': ('company_name','country',  'first_name', 'last_name', 'job_title', 'company_type',
                       'website', 'budget_for_events',  'weddings_per_year'),
        }),
        ('Destinations of Interest', {
            'fields': ( 'asia_pacific', 'middle_east_africa', 'europe', 'north_america', 'canada',
                  'south_central_america', 'caribbean')

        }),
        ("Is active?", {
            'fields': ('is_active',)
        })

    )

    actions = [mark_active, mark_inactive]


# class VendorMeetingRegisterAdmin(admin.ModelAdmin):
#     list_display = ('first_name', 'last_name', 'company_name', 'email', 'create_time')
#     list_filter = ('create_time',)
#     search_fields = ('first_name', 'last_name', 'company_name', 'email')
#     filter_horizontal = ('vendors',)
#
#     actions = ['export_as_csv']
#
#     def export_as_csv(self, request, queryset):
#         response = HttpResponse(content_type='text/csv')
#         response['Content-Disposition'] = 'attachment; filename="vendor_meeting_register.csv"'
#
#         writer = csv.writer(response)
#         writer.writerow(['First Name', 'Last Name', 'Company Name', 'Email', 'Create Time', 'Vendors'])
#
#         for obj in queryset:
#             vendors = ', '.join([vendor.company_name for vendor in obj.vendors.all()])
#             writer.writerow([obj.first_name, obj.last_name, obj.company_name, obj.email, obj.create_time, vendors])
#
#         return response

    # export_as_csv.short_description = "Export selected as CSV"


#working 8-05-2024 code
class VendorMeetingRegisterAdmin(admin.ModelAdmin):

    list_display = ('first_name', 'last_name', 'company_name', 'email', 'create_time')
    list_filter = ('create_time',)
    search_fields = ('first_name', 'last_name', 'company_name', 'email')
    filter_horizontal = ('vendors',)

    actions = ['export_as_csv','export_as_excel', 'export_mutual_conditions']

    def export_as_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="vendor_meeting_register.csv"'

        writer = csv.writer(response)

        # Headers
        headers = ['First Name', 'Last Name', 'Company Name', 'Email']
        selected_vendors = set()

        # Collect all selected vendors from queryset
        for obj in queryset:
            selected_vendors.update([vendor.company_name for vendor in obj.vendors.all()])

        # Add each selected vendor as a separate column in the headers
        headers.extend(selected_vendors)
        writer.writerow(headers)

        # Write data
        for obj in queryset:
            row = [
                obj.first_name,
                obj.last_name,
                obj.company_name,
                obj.email,
            ]

            row_selected_vendors = set([vendor.company_name for vendor in obj.vendors.all()])
            for vendor in selected_vendors:
                row.append('V' if vendor in row_selected_vendors else '')

            writer.writerow(row)

        return response
    export_as_csv.short_description = "Export selected as CSV"

    # def export_mutual_conditions(self, request, queryset):
    #     response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    #     response['Content-Disposition'] = 'attachment; filename="mutual_conditions.xlsx"'
    #
    #     wb = Workbook()
    #     ws = wb.active
    #     ws.title = "Mutual Conditions"
    #
    #     # Define headers
    #     headers = ['Vendor First Name', 'Vendor Last Name', 'Vendor Company Name']
    #
    #     # Collect all unique Vendor Meeting Register company names
    #     vendor_meeting_register_companies = VendorMeetingRegister.objects.values_list('company_name',
    #                                                                                   flat=True).distinct()
    #     headers.extend(vendor_meeting_register_companies)
    #     ws.append(headers)
    #
    #     # Get all delegate meeting records
    #     delegates = DelegateMeetingRegister.objects.all()
    #     # get all Delegate records
    #
    #     # Write data rows for each vendor
    #     for vendor in VendorPlanner.objects.all():
    #         row = [
    #             vendor.first_name,
    #             vendor.last_name,
    #             vendor.company_name,
    #         ]
    #
    #         for company_name in vendor_meeting_register_companies:
    #             mutual_found = False
    #
    #             # Check if the vendor's company name is in the list of company names
    #             if company_name in [delegate.company_name for delegate in delegates]:
    #                 # Check if the vendor matches any delegate by first name, last name, and company name
    #                 for delegate in delegates:
    #                     if (
    #                             vendor.first_name == delegate.first_name and
    #                             vendor.last_name == delegate.last_name and
    #                             vendor.company_name == delegate.company_name and
    #                             company_name == delegate.company_name
    #                     ):
    #                         mutual_found = True
    #                         break
    #
    #             # Append 'M' if mutual condition is satisfied or empty if not
    #             row.append('M' if mutual_found else '')
    #
    #         ws.append(row)
    #
    #     wb.save(response)
    #     return response
    #
    # export_mutual_conditions.short_description = "Export Mutual Conditions"

    # def export_mutual_conditions(self, request, queryset):
    #     response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    #     response['Content-Disposition'] = 'attachment; filename="mutual_conditions.xlsx"'
    #
    #     wb = Workbook()
    #     ws = wb.active
    #     ws.title = "Mutual Conditions"
    #
    #     # Define headers
    #     headers = [
    #         'Vendor First Name',
    #         'Vendor Last Name',
    #         'Vendor Company Name',
    #     ]
    #
    #     # Collect all unique Vendor Meeting Register company names
    #     vendor_meeting_register_companies = VendorMeetingRegister.objects.values_list('company_name',
    #                                                                                   flat=True).distinct()
    #     headers.extend(vendor_meeting_register_companies)
    #     ws.append(headers)
    #
    #     # Get all delegate meeting records
    #     delegates = DelegateMeetingRegister.objects.all()
    #
    #     # Write data rows for each vendor
    #     for vendor in VendorPlanner.objects.all():
    #         row = [
    #             vendor.first_name,
    #             vendor.last_name,
    #             vendor.company_name,
    #         ]
    #
    #         for company_name in vendor_meeting_register_companies:
    #             mutual_found = False
    #
    #             # Iterate through each delegate to perform the checks
    #             for delegate in delegates:
    #                 # First condition: vendor and delegate match by first name, last name, and company name
    #                 if (vendor.first_name == delegate.first_name and
    #                         vendor.last_name == delegate.last_name and
    #                         vendor.company_name == delegate.company_name):

    #                     # Additional checks:
    #                     # 1. Check if the delegate's company name is in the selected vendors
    #                     vendor_in_delegate_register = delegate.company_name in queryset.values_list('company_name',
    #                                                                                                 flat=True)
    #
    #                     # 2. Check if the vendor's company name is in the delegate meeting register
    #                     delegate_in_vendor_register = vendor.company_name in DelegateMeetingRegister.objects.filter(
    #                         company_name=delegate.company_name).values_list('company_name', flat=True)
    #
    #                     # Both conditions must be true for mutual condition to be valid
    #                     if vendor_in_delegate_register and delegate_in_vendor_register:
    #                         mutual_found = True
    #                     break
    #
    #             # Append 'M' if mutual condition is satisfied or empty if not
    #             row.append('M' if mutual_found else '')
    #
    #         ws.append(row)
    #
    #     wb.save(response)
    #     return response
    #
    # export_mutual_conditions.short_description = "Export Mutual Conditions"

    # def export_mutual_conditions(self, request, queryset):
    #     response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    #     response['Content-Disposition'] = 'attachment; filename="mutual_conditions.xlsx"'
    #
    #     wb = Workbook()
    #     ws = wb.active
    #     ws.title = "Mutual Conditions"
    #
    #     # Define headers
    #     headers = ['Vendor First Name', 'Vendor Last Name', 'Vendor Company Name']
    #
    #     # Collect all unique Vendor Meeting Register company names
    #     vendor_meeting_register_companies = VendorMeetingRegister.objects.values_list('company_name',
    #                                                                                   flat=True).distinct()
    #     headers.extend(vendor_meeting_register_companies)
    #     ws.append(headers)
    #
    #     # Get all delegate meeting records
    #     delegates = DelegateMeetingRegister.objects.all()
    #
    #     # Write data rows for each vendor
    #     for vendor in VendorPlanner.objects.all():
    #         row = [
    #             vendor.first_name,
    #             vendor.last_name,
    #             vendor.company_name,
    #         ]
    # #
    #         for company_name in vendor_meeting_register_companies:
    #             mutual_found = False
    #
    #             # Check if the vendor's meeting register company matches any delegate's company
    #             for delegate in delegates:
    #                 # First condition: vendor and delegate match by first name, last name, and company name
    #                 if (vendor.first_name == delegate.first_name and
    #                         vendor.last_name == delegate.last_name and
    #                         vendor.company_name == delegate.company_name ):
    #
    #
    #                     mutual_found = True
    #                     break
    # #
    #                 # Additional condition: delegate company name in selected vendors and vendor company name in selected delegates
    #                 if (delegate.company_name in [v.company_name for v in queryset] and
    #                         vendor.company_name in [d.company_name for d in
    #                                                 DelegateMeetingRegister.objects.filter(delegate__in=delegates)]):
    #                     mutual_found = True
    #                     break
    #
    #             # Represent mutual condition with 'M'
    #             row.append('M' if mutual_found else '')
    #
    #         ws.append(row)
    #
    #     wb.save(response)
    #     return response
    #
    # export_mutual_conditions.short_description = "Export Mutual Conditions"

    # excel working like my conditions

    # def export_mutual_conditions(self, request, queryset):
    #     response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    #     response['Content-Disposition'] = 'attachment; filename="mutual_conditions.xlsx"'
    #
    #     wb = Workbook()
    #     ws = wb.active
    #     ws.title = "Mutual Conditions"
    #
    #     # Define headers
    #     headers = ['Vendor First Name', 'Vendor Last Name', 'Vendor Company Name']
    #
    #     # Collect all unique Vendor Meeting Register company names
    #     vendor_meeting_register_companies = VendorMeetingRegister.objects.values_list('company_name',
    #                                                                                   flat=True).distinct()
    #     headers.extend(vendor_meeting_register_companies)
    #     ws.append(headers)
    #
    #     # Get all delegate meeting records
    #     delegates = DelegateMeetingRegister.objects.all()
    #
    #     # Write data rows for each vendor
    #     for vendor in VendorPlanner.objects.all():
    #         row = [
    #             vendor.first_name,
    #             vendor.last_name,
    #             vendor.company_name,
    #         ]
    #
    #         for company_name in vendor_meeting_register_companies:
    #             mutual_found = False
    #
    #             # Check if the vendor's meeting register company matches any delegate's company
    #             for delegate in delegates:
    #                 if (
    #                         vendor.first_name == delegate.first_name and
    #                         vendor.last_name == delegate.last_name and
    #                         vendor.company_name == delegate.company_name
    #
    #                 ):
    #                     mutual_found = True
    #                     break
    #
    #             # Represent mutual condition with 'M'
    #             row.append('M' if mutual_found else '')
    #
    #         ws.append(row)
    #
    #     wb.save(response)
    #     return response
    #
    # export_mutual_conditions.short_description = "Export Mutual Conditions"








admin.site.register(VendorMeetingRegister, VendorMeetingRegisterAdmin)
admin.site.register(VendorPlanner, VendorPlannerAdmin)
