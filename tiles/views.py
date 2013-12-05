# -*- coding: utf-8 -*-
from django.template import loader, Context, RequestContext, Template
from django.http import HttpResponse
from models import *
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt

def view(request, slug):
    try:
        sl = TileSet.objects.get(slug=slug)
    except:
        raise Http404

    var = Tile.objects.filter(set=sl)
    t = loader.get_template("tile.html")
    c = RequestContext(request, { 'var':var,})
    return HttpResponse(t.render(c))

def show(request, slug, id):
    tile = ContentTile.objects.get(pk=id)
    t = loader.get_template("tile_content.html")
    c = RequestContext(request, {'tile':tile,})
    return HttpResponse(t.render(c))