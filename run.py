from sys import exit
from decouple import config
from config import config_dict
from app import create_app, celery

DEBUG = config('DEBUG', default=True, cast=bool)

# The configuration
get_config_mode = 'Debug' if DEBUG else 'Production'

try:

    # Load the configuration using the default values
    app_config = config_dict[get_config_mode.capitalize()]

except KeyError:
    exit('Error: Invalid <config_mode>. Expected values [Debug, Production] ')

celery = celery
app = create_app(app_config)
app.app_context().push()

if __name__ == "__main__":
    app.run()
