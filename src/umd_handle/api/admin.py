from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.db.models import CharField, Value
from django.db.models.functions import Cast, Concat, LPad
from django.utils.html import format_html

from .models import Handle

# Customize the site header, title, and admin index page title
admin.site.site_header = "UMD Handle Service"
admin.site.site_title = "UMD Handle Service"
admin.site.index_title = "UMD Handle Service Admin Portal"

# Unregister User and Group, because authentication/authorization is controlled
# the Grouper, so there is no need to show these entries in the admin interface
admin.site.unregister(User)
admin.site.unregister(Group)


class HandleAdmin(admin.ModelAdmin):
    fields = [
        'prefix', 'suffix', 'url', 'repo', 'repo_id', 'description', 'notes',
        'created', 'modified',
    ]
    readonly_fields = ('suffix', 'created', 'modified')

    list_display = (
        'combined_handle', 'url_link', 'repo', 'repo_id', 'modified'
    )
    # Default order for admin list - modified descending
    ordering = ['-modified']

    search_fields = [
        'prefix', 'suffix', 'url', 'repo', 'repo_id', 'description', 'notes'
    ]

    def get_queryset(self, request):
      queryset = super().get_queryset(request)

      # Modify the the "Handle" (prefix/suffix) combination sorting to ensure
      # that the suffixes are sorted numerically by left-padding with zero
      # out to 10 digits (the approximate max length of the IntegerField).
      return queryset.annotate(
          _handle_sort_key=Concat(
              'prefix',
              # Pad the string representation of suffix with up to 10 leading zeros
              LPad(Cast('suffix', output_field=CharField()), Value(10), Value('0')),
              output_field=CharField()
          )
      )


    list_filter = ('repo', 'created', 'modified')

    @admin.display(description='URL', ordering='url')
    def url_link(self, obj):
        return format_html('<a href="{url}">{url}</a>', url=obj.url)

    @admin.display(description='Handle', ordering='_handle_sort_key')
    def combined_handle(self, obj):
        return str(obj)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            # Editing an existing handle
            return ('prefix',) + self.readonly_fields
        else:
            # Creating a new handle
            return self.readonly_fields

admin.site.register(Handle, HandleAdmin)
