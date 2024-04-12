import enum

class OndcAction(enum.Enum):
    SEARCH = "search"
    SELECT = "select"
    INIT = "init"
    CONFIRM = "confirm"
    CANCEL = "cancel"
    CANCELLATION_REASONS = "cancellation_reasons"
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
    ON_CANCELLATION_REASONS = "on_cancellation_reasons"
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
