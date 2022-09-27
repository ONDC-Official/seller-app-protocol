import traceback

# from flask_expects_json import expects_json
# from jsonschema.exceptions import ValidationError
#
#
# def expects_json_handling_validation(*args, **kwargs):
#     try:
#         return expects_json(*args, **kwargs)
#     except:
#         print("comig here")
from main.logger.custom_logging import log_error


def check_for_exception(func):
    def _wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            log_error("Something went wrong!")
            return {"error": str(e)}

    return _wrapper
