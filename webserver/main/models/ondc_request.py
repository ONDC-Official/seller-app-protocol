import enum

from main.models.init_database import dbBase
from sqlalchemy import Column, Integer, String, DateTime, Enum, Float, JSON

collection_names = ["on_search_items", "on_select", "on_init", "on_confirm", "on_cancel", "on_issue", "on_status", "on_support",
                    "on_track", "on_update", "on_issue_status"]


class OndcAction(enum.Enum):
    SEARCH = "search"
    SELECT = "select"
    INIT = "init"
    CONFIRM = "confirm"
    CANCEL = "cancel"
    STATUS = "status"
    SUPPORT = "support"
    TRACK = "track"
    UPDATE = "update"
    RATING = "rating"
    ISSUE = "issue"
    ISSUE_STATUS = "issue_status"
    ON_SEARCH = "on_search"
    ON_SELECT = "on_select"
    ON_INIT = "on_init"
    ON_CONFIRM = "on_confirm"
    ON_CANCEL = "on_cancel"
    ON_STATUS = "on_status"
    ON_SUPPORT = "on_support"
    ON_TRACK = "on_track"
    ON_UPDATE = "on_update"
    ON_RATING = "on_rating"
    ON_ISSUE = "on_issue"
    ON_ISSUE_STATUS = "on_issue_status"


class OndcDomain(enum.Enum):
    RETAIL = "retail"
    LOGISTICS = "logistics"


class OndcRequest(dbBase):
    __tablename__ = 'ondc_request'
    id = Column(Integer, primary_key=True)
    action = Column(Enum(OndcAction))
    domain = Column(Enum(OndcDomain))
    message_id = Column(String(50))
    request = Column(JSON)
    created_at = Column(DateTime)
