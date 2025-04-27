from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import DSC_class, Platform, IssuingAuth, Entity, LicensePeriod, Forms, Type, Status, DSCMaster, InOut, Docs, Shelf, DSCRenewal,UsageLogs,DSCEntity,CustomUser,DSCExtraField,DSCExtraData,EmailTemplate

# Register your models here.


admin.site.register(DSC_class)
admin.site.register(Platform)
admin.site.register(IssuingAuth)
admin.site.register(Entity)
admin.site.register(LicensePeriod)
admin.site.register(Forms)
admin.site.register(Type)
admin.site.register(Status)

admin.site.register(DSCMaster)
admin.site.register(InOut)

admin.site.register(Docs)

admin.site.register(DSCRenewal)
admin.site.register(Shelf)
admin.site.register(UsageLogs)


admin.site.register(DSCEntity)

admin.site.register(CustomUser)
admin.site.register(DSCExtraField)
admin.site.register(DSCExtraData)

@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ('template_type', 'last_modified')
    readonly_fields = ('last_modified',)