"""Core types
"""

from .command import *
import yaml


class VariantReference():
    """VariantReference
    """
    def __init__(self, kind, value):
        self.kind = kind
        self.value = value


def make_refs_dict(ref_specs):
    """Make refs dict
    """
    refs = {}
    for kind, sel_dict in ref_specs.items():
        for name, sel in sel_dict.items():
            refs[name] = VariantReference(kind, sel)
    return refs


class Direction():
    """Instruction data set that corresponds a whole YAML data.
    """
    required_key_set = {
        'version',
        'procs',
    }
    option_key_set = {
        'common',
        'refs',
    }

    @classmethod
    def load_spec(cls, data):
        """Return direction spec converted from parsed data
        """
        if not isinstance(data, dict):
            raise Exception('Direction source data is not dict')
        if not validate_keys(data, cls.required_key_set, cls.option_key_set):
            raise Exception('Direction keys are not valid.')
        allowed_key_set = cls.required_key_set | cls.option_key_set
        spec = {k: v for k, v in data.items() if k in allowed_key_set}
        return spec

    def __init__(self, data):
        self.spec = self.load_spec(data)
        self.version = self.spec['version']
        self.common = self.spec.get('common', {})
        self.procs = []
        for p_spec in self.spec['procs']:
            merged_spec = dict(common=self.common)
            merged_spec.update(p_spec)
            self.procs.append(Procedure(merged_spec))

    def __repr__(self):
        return '<Direction: version={}, procs({})>'.format(self.version, len(self.procs))


class Procedure():
    """Intentional operation group executing by browser
    """
    required_key_set = {
        'name',
        'commands',
    }
    option_key_set = {
        'desc',
        'refs',
        'interval',
        'common',
        'base_url',
    }

    @classmethod
    def load_spec(cls, data):
        """Return procedure spec converted from source data
        """
        if not isinstance(data, dict):
            raise Exception('Procedure source data is not dict {}'.format(type(data)))
        if not validate_keys(data, cls.required_key_set, cls.option_key_set):
            raise Exception('Procedure keys are not valid.')
        allowed_key_set = cls.required_key_set | cls.option_key_set
        spec = {k: v for k, v in data.items() if k in allowed_key_set}
        return spec

    def __init__(self, data, **kwargs):
        spec = Procedure.load_spec(data)
        self.spec = spec
        self.name = spec['name']
        self.common = spec.get('common', {})
        self.refs = make_refs_dict(self.common.get('refs', {}))
        self.refs.update(make_refs_dict(spec.get('refs', {})))
        self.desc = spec.get('desc', '')
        self.interval = spec.get('interval', 0)
        self.commands = []
        for c_src in spec['commands']:
            cmd = create_command(c_src, self.common, self.refs)
            self.commands.append(cmd)

    def __repr__(self):
        return '<Procedure: {}, refs({}), commands({})>'.format(self.name, len(self.refs), len(self.commands))


def load_yaml(filename):
    """Return parsed data
    """
    with open(filename, 'r+') as fp:
        data = yaml.load(fp)
    return data


def validate_keys(data, required_keys, option_keys=None):
    """Validate whether data dict has required_keys and other keys are in option_keys
    """
    key_set = set(data.keys())
    required_set = set(required_keys)
    is_ok = (required_set - key_set) == set()
    if is_ok and option_keys:
        option_set = set(option_keys)
        is_ok = (key_set - required_set - option_set) == set()
    return is_ok
