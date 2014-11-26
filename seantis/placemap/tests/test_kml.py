from seantis.placemap import tests
from seantis.placemap import utils


class TestKML(tests.IntegrationTestCase):

    def test_kml_fixes(self, map=None):
        self.assertEqual(
            utils.fix_common_kml_problems('type="xsd:string"'),
            'type="string"'
        )
