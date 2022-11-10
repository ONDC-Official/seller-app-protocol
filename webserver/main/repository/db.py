from main.logger.custom_logging import log, log_error
from main.models.init_database import db_session
from main.models.ondc_request import OndcRequest
from main.utils.date_utils import get_current_time_utc


def handle_sql_error(func):
    def wraps(*args,**kwargs):
        try:
            return func(*args,**kwargs)
        except Exception as e:
            log_error(e)
            db_session.rollback()
            return False
    return wraps


@handle_sql_error
def add_ondc_request(domain, action, message_id, request):
    ondc_request = OndcRequest(action=action, domain=domain, message_id=message_id, request=request,
                               created_at=get_current_time_utc())
    db_session.add(ondc_request)
    db_session.commit()
    return True


def get_ondc_requests(domain, action, message_id):
    ondc_requests = db_session.query(OndcRequest).filter_by(action=action, domain=domain, message_id=message_id)
    ondc_requests = [r.request for r in ondc_requests]
    return ondc_requests


def get_first_ondc_request(domain, action, message_id):
    ondc_request = db_session.query(OndcRequest).filter_by(action=action, domain=domain, message_id=message_id).first()
    return ondc_request.request

