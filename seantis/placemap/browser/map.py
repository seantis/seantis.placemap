from five import grok

from seantis.placemap.browser import BaseView
from seantis.placemap.interfaces import IMap


class MapView(BaseView):

    permission = 'zope2.View'
    grok.require(permission)
    grok.context(IMap)
    grok.name('view')

    template = grok.PageTemplateFile('templates/map.pt')
