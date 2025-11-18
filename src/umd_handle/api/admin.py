from django.contrib import admin

from .models import Handle

class HandleAdmin(admin.ModelAdmin):
    fields = [
        'prefix', 'suffix', 'url', 'repo', 'repo_id', 'description', 'notes',
        'created', 'modified',
    ]
    readonly_fields = ('suffix', 'created', 'modified')

    list_display = (
        'prefix', 'suffix', 'url', 'repo', 'repo_id', 'modified'
    )
    # Default order for admin list - modified descending
    ordering = ['-modified']

    search_fields = [
        'prefix', 'suffix', 'url', 'repo', 'repo_id', 'description', 'notes'
    ]

    list_filter = ('repo', 'created', 'modified')

    def get_readonly_fields(self, request, obj=None):
        if obj:
            # Editing an existing handle
            return ('prefix',) + self.readonly_fields
        else:
            # Creating a new handle
            return self.readonly_fields

admin.site.register(Handle, HandleAdmin)
