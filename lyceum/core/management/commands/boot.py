import importlib

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    command_dir = "core.management.commands.alias"

    def __init__(self, *args, **kwargs):
        self.module = importlib.import_module(self.command_dir)
        self.commands = self.get_instances()
        self.commands = sorted(
            self.commands,
            key=lambda instance: instance.priority,
        )
        super().__init__(*args, **kwargs)

    def add_arguments(self, parser):
        for instance in self.commands:
            instance.add_arguments(parser)

    def handle(self, *args, **kwargs):
        for instance in self.commands:
            instance_name = (
                instance.verbose_name
                if instance.verbose_name
                else instance.__class__.__name__
            )
            self.stdout.write(f"Start working with command `{instance_name}`")
            instance.run(self, *args, **kwargs)
            self.stdout.write(f"Finish working with command `{instance_name}`")

    def get_instances(self):
        commands = []
        for instance in dir(self.module):
            try:
                obj = getattr(self.module, instance)()
                if (
                    isinstance(obj, SimpleCommand)
                    and instance != SimpleCommand.__name__
                ):
                    commands.append(obj)
            except Exception:
                pass
        return commands


class SimpleCommand:
    priority = 10
    verbose_name = ""

    def add_arguments(self, parser):
        pass

    def run(self, handler, *args, **options):
        pass


__all__ = []
