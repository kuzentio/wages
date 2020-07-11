from .base import *

from dotenv import load_dotenv
load_dotenv(
    dotenv_path=os.path.join(BASE_DIR, '../provision/nano', '.env'),
)

ALLOWED_HOSTS = ['*']
