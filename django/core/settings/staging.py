from .defaults import *

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

DEBUG = False
DEPLOY_ENVIRONMENT = Environment.STAGING

# configure sentry
sentry_sdk.init(
    dsn=SENTRY_DSN,
    release=RELEASE_VERSION,
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
    send_default_pii=True,
)


# EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
# EMAIL_FILE_PATH = '/shared/logs/mail.log'
EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"

MAILGUN_API_KEY = config.get("email", "MAILGUN_API_KEY")
MAILGUN_SENDER_DOMAIN = config.get(
    "email", "MAILGUN_SENDER_DOMAIN", fallback="mg.comses.net"
)
EMAIL_SUBJECT_PREFIX = config.get(
    "email", "EMAIL_SUBJECT_PREFIX", fallback="[staging.comses.net]"
)
EMAIL_USE_TLS = True

ALLOWED_HOSTS = [".comses.net"]

# security settings from manage.py check --deploy
# https://docs.djangoproject.com/en/2.0/ref/settings/#secure-proxy-ssl-header
BASE_URL = DEPLOY_ENVIRONMENT.base_url
# set up robots + sitemaps inclusion https://django-robots.readthedocs.io/en/latest/
ROBOTS_SITEMAP_URLS = [f"{BASE_URL}/sitemap.xml"]
# SILENCED_SYSTEM_CHECKS = ['captcha.recaptcha_test_key_error']

# set up robots + sitemaps inclusion https://django-robots.readthedocs.io/en/latest/
ROBOTS_SITEMAP_URLS = [f"{BASE_URL}/sitemap.xml"]


SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = True
# https://docs.djangoproject.com/en/2.0/ref/middleware/#http-strict-transport-security
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# https://docs.djangoproject.com/en/2.0/ref/settings/#secure-content-type-nosniff
SECURE_CONTENT_TYPE_NOSNIFF = True
# https://docs.djangoproject.com/en/2.0/ref/settings/#secure-browser-xss-filter
SECURE_BROWSER_XSS_FILTER = True
# https://docs.djangoproject.com/en/2.0/ref/settings/#session-cookie-secure
SESSION_COOKIE_SECURE = True
# https://docs.djangoproject.com/en/2.0/ref/settings/#csrf-cookie-secure
CSRF_COOKIE_SECURE = True
# https://docs.djangoproject.com/en/2.0/ref/clickjacking/
X_FRAME_OPTIONS = "DENY"


# hcaptcha config
HCAPTCHA_SITEKEY = config.get("captcha", "HCAPTCHA_SITEKEY", fallback="")
HCAPTCHA_SECRET = config.get("captcha", "HCAPTCHA_SECRET", fallback="")

WSGI_APPLICATION = "core.wsgi.application"

INSTALLED_APPS += [
    "anymail",
    "fixture_magic",
]

ANYMAIL = {
    "MAILGUN_API_KEY": MAILGUN_API_KEY,
    "MAILGUN_SENDER_DOMAIN": MAILGUN_SENDER_DOMAIN,
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "root": {
        "level": "WARNING",
        "handlers": ["comsesfile"],
    },
    "formatters": {
        "verbose": {
            # 'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
            "format": "%(asctime)s %(levelname)-7s %(name)s:%(funcName)s:%(lineno)d %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "djangofile": {
            "level": "WARNING",
            "class": "logging.handlers.WatchedFileHandler",
            "formatter": "verbose",
            "filename": os.path.join(LOG_DIRECTORY, "django.log"),
        },
        "comsesfile": {
            "level": "WARNING",
            "class": "logging.handlers.WatchedFileHandler",
            "formatter": "verbose",
            "filename": os.path.join(LOG_DIRECTORY, "comsesnet.log"),
        },
    },
    "loggers": {
        "django.db.backends": {
            "level": "ERROR",
            "handlers": ["djangofile", "console"],
            "propagate": False,
        },
        "django": {
            "level": "WARNING",
            "handlers": ["console", "djangofile"],
            "propagate": False,
        },
        "home": {
            "level": "WARNING",
            "handlers": ["comsesfile"],
            "propagate": False,
        },
        "library": {
            "level": "WARNING",
            "handlers": ["comsesfile"],
            "propagate": False,
        },
        "core": {
            "level": "WARNING",
            "handlers": ["comsesfile"],
            "propagate": False,
        },
    },
}
