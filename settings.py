# Django settings for simplebtt project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'db/db.sql'             # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Moscow'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'ru'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = '/home/apkawa/Code/test/django/simplebtt/media'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '@rm%zt9+f6clu8#@b#(b-ed62)1y&he0-k4&3vxj)vqhtqkky2'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'account.middleware.AuthKeyMiddleware',
)

ROOT_URLCONF = 'simplebtt.urls'

TEMPLATE_DIRS = (
'/home/apkawa/Code/test/django/simplebtt/templates',
'/home/apkawa/Code/test/django/simplebtt/templates/tracker',
'/home/apkawa/Code/test/django/simplebtt/account/templates',
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'simplebtt',
    'simplebtt.tracker',
)

ALLOWED_INCLUDE_ROOTS = ( '/tmp',)

FORCE_SCRIPT_NAME="" # http://softwaremaniacs.org/forum/django/3887/
APPEND_SLASH = True
#Setting reCAPTCHA

RECAPTCHA_PUB_KEY = "6LesqwQAAAAAAHRbpBe8T8H5xg3nc9WCoLukieyd"
RECAPTCHA_PRIVATE_KEY = "6LesqwQAAAAAADHCDy7NKYChjM-miI0ktmy2eI3T"

# django-accounts
ACCOUNT_DOMAIN = 'rcd.org.ru'
LOGIN_REDIRECT_URL = '/'# (default): redirect to this url after successful
'''
ACCOUNT_REGISTRATION (True): allow registration on site
ACCOUNT_ACTIVATION (True): require the activation via email
LOGIN_REDIRECT_URL (default): redirect to this url after successful
authentication.
ACCOUNT_CAPTCHA (False): show captcha in registration form
ACCOUNT_LOGIN_DEBUG (False): allow debugging authorization with user ID in the request GET params.
DEFAULT_FROM_EMAIL (default): email which will be filled to From header of every sended email
RE_USERNAME:
ACCOUNT_USERNAME_MIN_LENGTH (3):
ACCOUNT_USERNAME_MAX_LENGTH (20):
ACCOUNT_PASSWORD_MIN_LENGTH (5):
ACCOUNT_PASSWORD_MAX_LENGTH (15):
ACCOUNT_AUTH_KEY_TIMEOUT (60 * 60 * 24): number of seconds that newly generated auth key is valid
ACCOUNT_DEBUG_MAIL_DIR (None): debug dir into which mail dumps will be saved
ACCOUNT_DOMAIN (fix.your.settings.com): domain of the site
'''


