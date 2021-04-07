# Data Dictionary Settings
import os
from dotenv import load_dotenv

load_dotenv()

# App Home is where this settings file is located
APP_HOME = os.path.dirname(os.path.abspath(__file))

# Where to find shared yml files, defaults to ./shared unless overridden by envvar
SHARED_DIR = os.getenv('SHARED_DIR', os.path.join(APP_HOME, 'shared'))

