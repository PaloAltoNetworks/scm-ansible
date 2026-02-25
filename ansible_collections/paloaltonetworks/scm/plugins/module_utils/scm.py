from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

META_FIELDS = frozenset([
    'state', 'client_id', 'client_secret', 'tsg_id',
    'id', 'folder', 'snippet', 'device',
])


def build_payload(module, param_to_field):
    """Build API payload from module params, using the per-module field mapping."""
    payload = {}
    for key, value in module.params.items():
        if value is not None and key not in META_FIELDS:
            api_key = param_to_field.get(key, key)
            payload[api_key] = value
    return payload


def get_container_params(module):
    """Extract container params (folder/snippet/device) from module params."""
    params = {}
    for key in ('folder', 'snippet', 'device'):
        val = module.params.get(key)
        if val:
            params[key] = val
    return params


def to_result_data(obj):
    """Convert SDK response object to dict, including the id field."""
    data = obj.to_dict() if hasattr(obj, 'to_dict') else {}
    if hasattr(obj, 'id') and obj.id is not None:
        data['id'] = obj.id
    return data


def _normalize_value(value):
    """Normalize a value for comparison."""
    if isinstance(value, list):
        if not value:
            return value
        # Lists of dicts: preserve order (rules, match_list, etc.)
        if isinstance(value[0], dict):
            return value
        # Lists of simple types: sort for order-insensitive comparison
        try:
            return sorted(value)
        except TypeError:
            return value
    return value


def fields_differ(existing, payload):
    """Check if any fields in the payload differ from the existing object.

    Handles list ordering for simple-value lists (tags, static members,
    source addresses, etc.) to avoid spurious updates when the API
    returns items in a different order than the user specified.
    """
    existing_dict = existing.to_dict() if hasattr(existing, 'to_dict') else {}
    for key, value in payload.items():
        existing_value = existing_dict.get(key)
        if _normalize_value(existing_value) != _normalize_value(value):
            return True
    return False
