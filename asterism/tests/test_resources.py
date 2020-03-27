from unittest import TestCase

from asterism.resources.archivesspace import (
    ArchivesSpaceArchivalObject,
    ArchivesSpaceResource,
    ArchivesSpaceAgentCorporateEntity,
    ArchivesSpaceAgentFamily,
    ArchivesSpaceAgentPerson)


class TestResources(TestCase):

    def test_resources(self):
        """Imports canonical classes to ensure everything is basically okay."""
        for resource in [
                ArchivesSpaceArchivalObject,
                ArchivesSpaceResource,
                ArchivesSpaceAgentCorporateEntity,
                ArchivesSpaceAgentFamily,
                ArchivesSpaceAgentPerson]:
            r = resource()
            self.assertTrue(isinstance(r, resource))
