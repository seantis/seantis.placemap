from collective.geo.mapwidget.maplayers import MapLayer
from plone.memoize.instance import memoizedproperty


class SourceLayer(MapLayer):
    """ A custom layer for placemap sources that extends the default with
    additional properties that are added to the javascript code.

    """

    js_template = """
        function() {
            return seantis.placemap.create_kml_layer('%(url)s', '%(title)s');
        }
    """

    @memoizedproperty
    def jsfactory(self):
        return self.js_template % dict(url=self.url, title=self.title)

    @staticmethod
    def from_source(source):
        layer = SourceLayer()

        layer.id = source.id
        layer.title = source.title
        layer.url = source.absolute_url() + '/kml-document'

        return layer
