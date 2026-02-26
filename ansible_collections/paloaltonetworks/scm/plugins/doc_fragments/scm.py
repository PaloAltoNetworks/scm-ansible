from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


class ModuleDocFragment(object):

    DOCUMENTATION = r'''
options:
    client_id:
        description:
            - OAuth2 Client ID for SCM authentication.
            - Can also be set via the C(SCM_CLIENT_ID) environment variable.
        required: False
        type: str
    client_secret:
        description:
            - OAuth2 Client Secret for SCM authentication.
            - Can also be set via the C(SCM_CLIENT_SECRET) environment variable.
        required: False
        type: str
        no_log: True
    tsg_id:
        description:
            - Tenant Service Group ID for SCM authentication.
            - Can also be set via the C(SCM_TSG_ID) environment variable.
        required: False
        type: str
'''
