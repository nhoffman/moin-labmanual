"""Print the version number of moinlm

"""

from MoinMoin import wikiutil

from moinlm import __version__

Dependencies = ["time"]


def main(macro, arg):

    request = macro.request
    msg = 'moinlm {}'.format(__version__)
    output = request.formatter.text(msg)
    return output


def execute(macro, args):
    try:
        return wikiutil.invoke_extension_function(
            macro.request, main,
            args, [macro])
    except ValueError, err:
        return macro.request.formatter.text(
            "<<LMVersion: %s>>" % err.args[0], style="color:red")
