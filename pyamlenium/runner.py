import sys
import time

from selenium import webdriver
from selenium.webdriver.common.by import By

from . import (
    Direction,
    Procedure,
    Command,
    load_yaml,
)


class DirectionRunner():
    def __init__(self, _dir):
        self.dir = _dir

    def run(self):
        """Run each procedures
        """
        for p in self.dir.procs:
            p_runner = ProcedureRunner(p)
            p_runner.run()


class ProcedureRunner():
    def __init__(self, proc):
        self.proc = proc

    def run(self):
        """Run each commands
        """
        driver = webdriver.Chrome()
        ctx = {}
        for cmd in self.proc.commands:
            print(cmd)
            prev = cmd.run(driver, ctx)
            ctx.update(prev=prev)
        driver.close()


def main(filename):
    """Main function
    """
    data = load_yaml(filename)
    direction = Direction(data)
    d_runner = DirectionRunner(direction)
    d_runner.run()


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print('YAML filename is required.')
        exit(0)
    args = sys.argv[1:]
    main(args[0])

