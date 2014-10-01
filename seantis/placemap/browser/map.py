from collective.geo.mapwidget.browser.widget import MapWidget
from five import grok
from plone import api
from plone.memoize.view import memoize

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
    def mapfields(self):
        assert self.show_map, """
            This should not be called if there are no sources.
        """

        widget = MapWidget(self, self.request, self.context)

        # the widget is stored somewhere by collective.geo so we
        # have to be sure to only add the source layers if not yet present
        new_sources = (
            s.getObject() for s in self.get_sources() if s.id not in set(
                layer.id for layer in widget._layers
            )
        )

        for source in new_sources:
            widget._layers.append(SourceLayer.from_source(source))

        return (widget, )

    @memoize
    def get_sources(self):
        folder_path = '/'.join(self.context.getPhysicalPath())
        catalog = api.portal.get_tool('portal_catalog')

        return catalog(
            path={'query': folder_path, 'depth': 1},
            portal_type='seantis.placemap.source'
        )
