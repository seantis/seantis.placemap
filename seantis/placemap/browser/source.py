from five import grok
from plone.autoform.form import AutoExtensibleForm
from plone.directives.dexterity import AddForm

from seantis.placemap import _
from seantis.placemap import utils
from seantis.placemap.browser.base import BaseForm, BaseView
from seantis.placemap.interfaces import ISource


class SourceBaseForm(BaseForm, AutoExtensibleForm):

    grok.baseclass()

    def before_save(self, data):
        data['kml'] = utils.fetch_kml_document(data['url'])

        if not data['kml']:
            self.raise_action_error(
                _(u"No KML-Document was found on the given url")
            )


class SourceAddForm(AddForm, SourceBaseForm):
    grok.name('seantis.placemap.source')

    grok.context(ISource)
    grok.require('cmf.AddPortalContent')

    schema = ISource


class SourceEditForm(SourceBaseForm):
    """ Provides an edit form for memberships in seantis.kantonsrat. Said
    form does not offer all fields. It namely removes the ability to change
    the referenced person.

    """
    grok.name('edit')

    grok.context(ISource)
    grok.require('cmf.ModifyPortalContent')

    schema = ISource


class SourceKmlView(BaseView):

    permission = 'zope2.View'
    grok.require(permission)
    grok.context(ISource)
    grok.name('kml-document')

    def render(self):
        self.request.response.setHeader(
            'Content-Disposition',
            'attachment; filename="%s"' % self.context.id
        )
        self.request.response.setHeader(
            'Content-Type',
            'application/vnd.google-earth.kml+xml; charset=utf-8'
        )

        return self.context.kml
