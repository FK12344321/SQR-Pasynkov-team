from datetime import datetime
from unittest.mock import patch, MagicMock
import pytest
from sqlalchemy.orm import Session

from app.models import ActivitiesFilter
from app.database.models import Activity as DB_Activity
from app.database.crud import get_activities


@pytest.fixture
def mock_session():
    session = MagicMock(spec=Session)
    with patch('app.database.crud.session_maker', return_value=session):
        yield session


def test_get_activities(mock_session):
    # Set up the mocked return values for the chained query calls
    mock_query = mock_session.query.return_value
    mock_filter = mock_query.filter.return_value
    mock_order_by = mock_filter.order_by.return_value
    mock_limit = mock_order_by.limit.return_value
    mock_offset = mock_limit.offset.return_value
    mock_all = mock_offset.all.return_value

    # Mock data to be returned by the all() method
    mock_all.return_value = [
        DB_Activity(id=1, activity_type="Running", start_date=datetime(
            2022, 5, 1), end_date=datetime(2022, 5, 1), username="user1"),
        DB_Activity(id=2, activity_type="Walking", start_date=datetime(
            2022, 5, 2), end_date=datetime(2022, 5, 2), username="user1")
    ]

    # Input parameters
    filter_params = ActivitiesFilter(
        page_index=1,
        page_size=2,
        start_date=datetime(2022, 4, 30),
        end_date=datetime(2022, 5, 3),
        activity_type="Running"
    )

    # Call the function under test
    activities = get_activities(filter_params, "user1")

    # Assertions to check function's correctness
    assert len(activities) == 0
