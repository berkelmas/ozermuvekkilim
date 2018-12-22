from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _


from .models import User, Dava, Surec, DavaKarsiTaraf

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'birth_date')}),

        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    list_filter = ()

@admin.register(Dava)
class DavaAdmin(admin.ModelAdmin):

    list_display = ['dava_title', 'dava_esasno', 'get_muvekkiller', 'get_karsitaraflar']
    list_filter = ('dava_category', 'dava_mahkeme', 'dava_sifat')

    search_fields = ('dava_title', 'dava_esasno', 'davakarsitaraf__davakarsitaraf_isim')
    ordering = ('-dava_start',)

    def get_muvekkiller(self, obj):
        return "\n".join([p.email for p in obj.user.all()])
    get_muvekkiller.short_description = 'Müvekkil Adı'

    def get_karsitaraflar(self, obj):
        return "\n".join([p.davakarsitaraf_isim for p in obj.davakarsitaraf.all()])
    get_karsitaraflar.short_description = 'Karşı Taraf'

@admin.register(Surec)
class SurecAdmin(admin.ModelAdmin):

    list_display = ['surec_title', 'get_esas']

    search_fields = ('surec_title', 'dava__dava_esasno')

    def get_name(self, obj):
        return obj.dava.dava_title
    get_name.admin_order_field  = 'dava_start'  #Allows column order sorting
    get_name.short_description = 'Dava Adı'  #Renames column head

    def get_esas(self, obj):
        return obj.dava.dava_esasno
    get_esas.short_description = 'Dava Esas Numarası'

from django.contrib.auth.models import Group
admin.site.unregister(Group)


admin.site.register(DavaKarsiTaraf)
admin.site.site_header = "Salt Hukuk Avukat Paneli "
admin.site.site_title = "Salt Hukuk Admin Paneli "
admin.site.index_title = "Yönetim Paneli"

