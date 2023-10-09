from django.contrib import admin

from .models import Directory, File, Firmware

class FirmwareAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'name', 'admin', 'admin_org', 'status')
    list_filter = ('status', 'admin_org')
    search_fields = ('name', 'admin__username', 'admin_org__name')
    # date_hierarchy = 'created'
    # readonly_fields = ('uuid')

admin.site.register(Firmware, FirmwareAdmin)

class DirectoryAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'name', 'owner', 'group', 'created', 'modified')
    list_filter = ('owner', 'group')
    search_fields = ('name', 'owner', 'group')
    # date_hierarchy = 'created'
    readonly_fields = ('uuid','files','directories','path','rpath')
admin.site.register(Directory, DirectoryAdmin)

class FileAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'name', 'owner', 'group', 'created', 'modified')
    list_filter = ('owner', 'group')
    search_fields = ('name', 'owner', 'group')
    # date_hierarchy = 'created'
    readonly_fields = ('uuid','path','rpath')
admin.site.register(File, FileAdmin)

