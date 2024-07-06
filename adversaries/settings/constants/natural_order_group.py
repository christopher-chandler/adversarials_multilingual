# Standard
# None

# Pip
import click

# Custom
# None


class NaturalOrderGroup(click.Group):
    """
    Die Anordnung der Commands so ausgeben, dass sie der Reihenfolge
    widerspiegeln, die im Code vorkommt.

    cls -> Commands werden so angegeben, wie sie im Quellcode erscheinen
    name -> Name des Programms
    add_completion -> entfernt "
    --install-completion  Install completion for the current shell. "
    """

    def list_commands(self, ctx):
        return self.commands.keys()


if __name__ == "__main__":
    pass
