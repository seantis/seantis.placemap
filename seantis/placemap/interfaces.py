from plone.directives import form
from zope import schema
from zope.interface import Interface

from seantis.placemap import _
from seantis.plonetools.schemafields import Website


class ISeantisPlacemapSpecific(Interface):
    pass


class IPlacemap(form.Schema):
    """ Contains the urls to the kml documents. """

    title = schema.TextLine(
        title=_(u"Name of the placemap"),
        required=True
    )


class IPlacemapSource(form.Schema):
    """ Defines the source of a kml document and describes features like
    the icon to use for placemarks or the color to use for lines.

    """

    title = schema.TextLine(
        title=_(u"Name of the source"),
        required=True
    )

    url = Website(
        title=_(u"URL of KML Document"),
        required=True
    )
