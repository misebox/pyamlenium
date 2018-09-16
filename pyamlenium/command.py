
"""
"""
import abc
import copy

from selenium.webdriver.remote.webelement import WebElement


class Command():
    """A command that is unita of execution.
    """
    __metaclass__ = abc.ABCMeta
    def __init__(self, spec, **kwargs):
        self.spec = spec
        self.act = spec.get('act')
        self.opt = spec.get('opt')
        self.key = ''

    def get_key(self):
        return self.key

    def __repr__(self):
        return '<{}: {}>'.format(type(self).__name__, self.opt)

    @abc.abstractmethod
    def run(self, browser, ctx=None):
        """Subclass of Command class overrides this method.
        """
        raise NotImplementedError()


class GoCommand(Command):
    key = 'go'
    def run(self, browser, ctx=None):
        """Request specified URL
        """
        path = self.opt
        base_url = self.spec.get('base_url', '')
        # TODO: URL should be joined safety as URL
        url = base_url + path
        print('url:', url)
        browser.get(url)
        return url


class FindCommand(Command):
    key = 'find'
    def run(self, browser, ctx=None):
        """Find an element and return it.
        """
        from .core import VariantReference
        opt = self.opt
        elm = None
        base_element = ctx.get('base_element')
        base = base_element if isinstance(base_element, WebElement) else browser
        if isinstance(opt, VariantReference):
            if opt.kind == 'css':
                elm = base.find_element_by_css_selector(opt.value)
        else:
            print('Something wrong', opt)
        return elm


class ClickCommand(Command):
    key = 'click'
    """Subclass of Command class
    """
    def run(self, browser, ctx=None):
        """Click an element and return it through.
        """
        base_element = ctx.get('base_element')
        base = base_element if isinstance(base_element, WebElement) else browser
        opt = self.opt
        target = base.find_element_by_css_selector(opt.value)
        if isinstance(target, WebElement):
            target.click()
        return target


class SendKeysCommand(Command):
    key = 'send_keys'
    def run(self, browser, ctx=None):
        """Send keys
        """
        prev = ctx.get('prev')
        opt = self.opt
        if isinstance(prev, WebElement):
            prev.send_keys(opt)
        return prev


class SetContextCommand(Command):
    key = 'set_context'
    def run(self, browser, ctx=None):
        """Set context
        """
        if isinstance(self.opt, dict):
            ctx['base_element'] = self.opt
        return ctx.get('prev')


command_dict = {
    c.key: c for c in (
        GoCommand,
        FindCommand,
        SendKeysCommand,
        ClickCommand,
        SetContextCommand,
    )
}
def create_command(data, common, refs):
    """Create intent command
    """
    spec = dict(common)
    spec.update(load_spec(data, refs))
    act = spec.get('act')
    return command_dict.get(act, Command)(spec)


def load_spec(data, refs):
    """Return command spec converted from parsed data
    """
    spec = {}
    items = list(data.items())
    item = items[0]
    act, opt = item
    spec.update(act=act)
    if isinstance(opt, dict):
        print('Dict')
        spec.update(**opt)
    elif isinstance(opt, str):
        spec.update(opt=opt)
    else:
        print('Something wrong')
    for k, v in spec.items():
        if v in refs:
            spec[k] = refs[v]
    return spec
