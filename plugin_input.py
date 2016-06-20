import os
import urllib.parse

from evarify import ConfigStore, EnvironmentVariable
from evarify.filters.python_basics import validate_is_not_none, value_to_none


def validate_devpi_server_url(config_val, evar):
    parsed = urllib.parse.urlsplit(config_val)
    if not all([parsed.scheme, parsed.netloc]):
        raise ValueError(
            "You must specify the full, absolute URI to your devpi server "
            "(including ).: %s", config_val)
    return config_val


values = ConfigStore({
    'SERVER': EnvironmentVariable(
        name='PLUGIN_SERVER',
        filters=[
            value_to_none, validate_is_not_none, validate_devpi_server_url
        ],
        help_txt=(
            "Full path to the root of the devpi server. Make sure to include "
            "the protocol (and port if it's not standard)."
        )
    ),
    'INDEX': EnvironmentVariable(
        name='PLUGIN_INDEX',
        filters=[value_to_none, validate_is_not_none],
        help_txt="The <user>/<repo> combo designating the index to upload to.",
    ),
    'USERNAME': EnvironmentVariable(
        name='PLUGIN_USERNAME',
        filters=[value_to_none, validate_is_not_none],
        help_txt="The devpi username to login with before uploading.",
    ),
    'PASSWORD': EnvironmentVariable(
        name='PLUGIN_PASSWORD',
        help_txt="The devpi user's password.",
    ),
    'PACKAGE_PATH': EnvironmentVariable(
        name='PLUGIN_PACKAGE_PATH',
        filters=[value_to_none, validate_is_not_none],
        default_val=os.getcwd(),
        help_txt="Path to the package to upload.",
    ),
})
