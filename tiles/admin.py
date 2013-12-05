from django.contrib import admin

from models import *

class TileSetAdmin(admin.ModelAdmin):
    list_display = ('slug',)


class LinkTileAdmin(admin.ModelAdmin):
    list_display = ('href',)


class FileTileAdmin(admin.ModelAdmin):
    list_display = ('document',)


class ContentTileAdmin(admin.ModelAdmin):
    list_display = ('content',)


admin.site.register(ContentTile,ContentTileAdmin)
admin.site.register(FileTile,FileTileAdmin)
admin.site.register(LinkTile,LinkTileAdmin)
admin.site.register(TileSet,TileSetAdmin)