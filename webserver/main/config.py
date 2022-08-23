import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    OTP_TIMEOUT_IN_MINUTES = 60
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious_secret_key')
    DEBUG = False
    COOKIE_EXPIRY = 60000
    PORT = 9900
    FLASKS3_BUCKET_NAME = os.getenv('static_bucket_name')
    FLASKS3_FILEPATH_HEADERS = {r'.css$': {'Content-Type': 'text/css; charset=utf-8'},
                                r'.js$': {'Content-Type': 'text/javascript'}}
    FLASKS3_ACTIVE = os.getenv("flask_s3_active", "True") == "True"
    FLASKS3_GZIP = True
    CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
    JWT_TOKEN_LOCATION = ['headers']
    S3_PRIVATE_BUCKET = os.getenv("PRIVATE_BUCKET")
    # below is valid for tokens coming in as part of query_params
    JWT_QUERY_STRING_NAME = "token"
    # Set the secret key to sign the JWTs with
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    BAP_DOMAIN = "nic2004:52110"
    BAP_CITY_CODE = "std:080"
    BAP_COUNTRY_CODE = "IND"
    BAP_ID = "box.beckn.org"
    BAP_TTL = "20"
    BECKN_SECURITY_ENABLED = False
    BAP_PRIVATE_KEY = "some-key"
    BAP_KEY_ID = "default-key"
    RABBITMQ_QUEUE_NAME = "bpp_protocol"
    RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
    BPP_CLIENT_ENDPOINT = "http://client-endpoint"


class DevelopmentConfig(Config):
    DEBUG = True
    ENV = True
    RABBITMQ_HOST = "localhost"


class ProductionConfig(Config):
    DEBUG = False
    RABBITMQ_HOST = "rabbitmq"


config_by_name = dict(
    dev=DevelopmentConfig,
    prod=ProductionConfig,
)

key = Config.SECRET_KEY


def get_config_by_name(config_name, default=None, env_param_name=None):
    config_env = os.getenv(env_param_name or "ENV")
    config_value = default
    if config_env:
        config_value = getattr(config_by_name[config_env](), config_name, default)
    return config_value


def get_email_config_value_for_name(config_name):
    email_config_value = get_config_by_name("SES") or {}
    config = email_config_value.get(config_name)
    return config
