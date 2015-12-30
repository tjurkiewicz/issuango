import pickle

import pytest

import utils


@pytest.mark.django_db
def test_pickle(issue):
    iac = utils.IssueAttributesContainer(issue)

    pickled = pickle.dumps(iac)
    new_iac = pickle.loads(pickled)

    assert new_iac.issue == issue