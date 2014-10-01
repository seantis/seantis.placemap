from five import grok
from plone import api
from plone.memoize.view import memoize

from seantis.placemap.browser import BaseView
from seantis.placemap.interfaces import IMap


class MapView(BaseView):

    permission = 'zope2.View'
    grok.require(permission)
    grok.context(IMap)
    grok.name('view')

    template = grok.PageTemplateFile('templates/map.pt')

    @property
    def show_map(self):
        return len(self.get_sources()) > 0

    @memoize
    def get_sources(self):
        folder_path = '/'.join(self.context.getPhysicalPath())
        catalog = api.portal.get_tool('portal_catalog')

        return catalog(
            path={'query': folder_path, 'depth': 1},
            portal_type='seantis.placemap.source'
        )
