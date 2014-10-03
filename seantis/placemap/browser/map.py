from collective.geo.mapwidget.browser.widget import MapWidget
from five import grok
from plone import api
from plone.memoize.view import memoize
from zope.security import checkPermission

from seantis.placemap.browser import BaseView
from seantis.placemap.browser.sourcelayer import SourceLayer
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

    @property
    def show_controls(self):
        """ Returns True if the sources should be modifyable/removeable. """

        # not exactly the required permission, but that's not the point:
        # if the user has the permission to edit the context the permission
        # to edit the sources probably inherited.
        return checkPermission('cmf.ModifyPortalContent', self.context)

    @property
    def mapfields(self):
        assert self.show_map, """
            This should not be called if there are no sources.
        """

        widget = MapWidget(self, self.request, self.context)
        widget._layers = tuple(
            SourceLayer.from_source(s) for s in self.get_sources()
        )

        return (widget, )

    @memoize
    def get_sources(self):
        folder_path = '/'.join(self.context.getPhysicalPath())
        catalog = api.portal.get_tool('portal_catalog')

        return catalog(
            path={'query': folder_path, 'depth': 1},
            portal_type='seantis.placemap.source'
        )
