#   Copyright 2007,2008,2009,2011 Everyblock LLC, OpenPlans, and contributors
#
#   This file is part of ebpub
#
#   ebpub is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   ebpub is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with ebpub.  If not, see <http://www.gnu.org/licenses/>.
#

from django.contrib.gis import admin
from ebpub.db.forms import LocationForm
from ebpub.db.forms import NewsItemForm
from ebpub.db.models import Attribute
from ebpub.db.models import Location
from ebpub.db.models import LocationSynonym
from ebpub.db.models import LocationType
from ebpub.db.models import Lookup
from ebpub.db.models import NewsItem
from ebpub.db.models import Schema
from ebpub.db.models import SchemaField
from ebpub.geoadmin import OSMModelAdmin

class AttributeInline(admin.StackedInline):
    # TODO: this badly needs a custom Form that takes into account the
    # Schema and shows you only relevant fields, with labels.
    model = Attribute

class NewsItemAdmin(OSMModelAdmin):
    inlines = [
        AttributeInline,
        ]

    list_display = ('title', 'schema', 'item_date', 'pub_date', 'location_name')
    raw_id_fields = ('location_object', 'block')
    list_filter = ('schema',)
    search_fields = ('title', 'description',)
    form = NewsItemForm

class LocationTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_browsable', 'is_significant')
    list_filter = ('is_browsable', 'is_significant')

class LocationAdmin(OSMModelAdmin):
    form = LocationForm
    list_filter = ('location_type', 'city', 'is_public',)
    list_display = ('name', 'location_type', 'creation_date', 'area')
    search_fields = ('name',)

    # This is populated by a trigger in ebpub/db/sql/location.sql.
    readonly_fields = ('area',)


class SchemaAdmin(admin.ModelAdmin):
    list_display = ('name', 'last_updated', 'importance', 'is_public',
                    'has_newsitem_detail',)

class SchemaFieldAdmin(admin.ModelAdmin):
    list_display = ('pretty_name',
                    'schema',
                    'display',
                    'datatype',
                    'real_name',
                    'is_filter', 'is_charted', 'is_searchable',
                    'is_lookup', 'is_many_to_many_lookup',
                    )
    list_filter = ('schema', 'display', 'is_lookup', 'is_filter',
                   'is_charted', 'is_searchable', 'real_name')


class LookupAdmin(admin.ModelAdmin):
    # TODO: this would make more sense to edit inline on NewsItem,
    # but that would require some custom wackiness.
    list_display = ('name', 'schema_field')
    search_fields = ('description', 'name', 'code')

class LocationSynonymAdmin(OSMModelAdmin):
    list_display = ('pretty_name', 'location')
    search_fields = ('pretty_name', 'location')

admin.site.register(Schema, SchemaAdmin)
admin.site.register(SchemaField, SchemaFieldAdmin)
admin.site.register(NewsItem, NewsItemAdmin)
admin.site.register(LocationType, LocationTypeAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(LocationSynonym, LocationSynonymAdmin)
admin.site.register(Lookup, LookupAdmin)
