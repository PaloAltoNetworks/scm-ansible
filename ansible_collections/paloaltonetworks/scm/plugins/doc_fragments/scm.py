from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


class ModuleDocFragment(object):

    DOCUMENTATION = r'''
short_description: Common authentication options for SCM modules
description:
    - This doc fragment provides common authentication parameters shared by all
      Palo Alto Networks Strata Cloud Manager (SCM) modules.
    - Credentials can be supplied as module parameters, environment variables,
      or via a JSON configuration file.
    - 'Resolution order: module parameter > environment variable > configuration file.'
options:
    client_id:
        description:
            - OAuth2 Client ID for SCM authentication.
            - Can also be set via the C(SCM_CLIENT_ID) environment variable.
            - Can also be set in a JSON configuration file (C(config/scm-config.json) or path specified by C(SCM_CONFIG_FILE)).
            - 'Resolution order: module parameter > environment variable > configuration file.'
        required: False
        type: str
    client_secret:
        description:
            - OAuth2 Client Secret for SCM authentication.
            - Can also be set via the C(SCM_CLIENT_SECRET) environment variable.
            - Can also be set in a JSON configuration file (C(config/scm-config.json) or path specified by C(SCM_CONFIG_FILE)).
            - 'Resolution order: module parameter > environment variable > configuration file.'
        required: False
        type: str
        no_log: True
    tsg_id:
        description:
            - Tenant Service Group ID for SCM authentication.
            - Can also be set via the C(SCM_TSG_ID) environment variable.
            - Can also be set in a JSON configuration file (C(config/scm-config.json) or path specified by C(SCM_CONFIG_FILE)).
            - 'Resolution order: module parameter > environment variable > configuration file.'
        required: False
        type: str
'''
