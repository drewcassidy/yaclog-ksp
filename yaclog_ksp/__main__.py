import click
import os.path
import yaclog
import re
import pathlib
from yaclog_ksp.cfgnode import ConfigNode


@click.command()
@click.option('-i', '--input', 'inpath',
              default='CHANGELOG.md', show_default=True,
              type=click.Path(readable=True, exists=True, dir_okay=False),
              help="Input markdown file to read from.")
@click.option('-o', '--output', 'outpath',
              default=None,
              type=click.Path(writable=True, dir_okay=False),
              help="Output file to write to. Uses 'GameData/{name}/Versioning/{name}ChangeLog.cfg' by default.")
@click.option('-n', '--name', help="The name of the mod. Derived from the current directory by default.")
@click.version_option()
def main(inpath, outpath, name):
    """ Converts markdown changelogs to KSP changelog configs."""
    if not name:
        # try to guess name from current directory
        pathname = pathlib.Path.cwd().name.removeprefix('KSP-')
        modslug = str.join('', [s.title() for s in re.split(r'[ _-]+', pathname)])
        segments = re.findall(r'[A-Z](?:[a-z]+|[A-Z]*(?=[A-Z]|$))', modslug)
        name = segments[0] + [' ' + s for s in segments[1:]]
    else:
        modslug = str.join('', [s.title() for s in re.split(r'[ _-]+', name)])

    if not outpath:
        # default is in GameData/{name}/Versioning/{name}ChangeLog.cfg
        outpath = pathlib.Path('GameData', modslug, 'Versioning', modslug + 'ChangeLog.cfg')

    log = yaclog.read(inpath)
    node = ConfigNode()

    # find metadata table rows
    for key, value in re.findall(r'^\|(?P<key>[^\n-]*?)\|(?P<value>[^\n-]*?)\|$', log.header, flags=re.MULTILINE):
        key = key.strip()
        value = value.strip()
        if key.strip(':-'):
            node.add_value(key, value)

    # if modname not in metadata, then add it here
    if not node.has_value('modName'):
        node.add_value('modName', name)

    # iterate through all versions
    for version in log.versions:
        v_node = node.add_new_node('VERSION')
        v_node.add_value('version', version.name)

        # add date
        if version.date:
            v_node.add_value('versionDate', str(version.date))

        # check for KSP version tag and add it
        for tag in version.tags:
            if match := re.match(r'KSP (?P<versionKSP>.*)', tag):
                v_node.add_value('versionKSP', match['versionKSP'])
                break

        # add entries
        for section, entries in version.sections.items():
            for entry in entries:

                bullets = re.findall(r'^[\t ]*[-+*] (.*?)$', entry, flags=re.MULTILINE)

                if len(bullets) < 1:
                    # not a bullet point, but a paragraph. all one string
                    change = entry.replace('\n', ' ')
                    subchanges = []
                else:
                    # bullet point, may have sub points
                    change = bullets[0]
                    subchanges = bullets[1:]

                if section or len(subchanges) > 0:
                    e_node = v_node.add_new_node('CHANGE')

                    if section:
                        # KerbalChangelog only actually cares about the first character,
                        # so dont bother correcting "Fixed"->"Fix", etc
                        e_node.add_value('type', section.title())

                    e_node.add_value('change', change)
                    for sc in subchanges:
                        e_node.add_value('subchange', sc)

                else:
                    v_node.add_value('change', change)

    with open(outpath, 'w') as fp:
        fp.write('KERBALCHANGELOG\n')
        fp.write(str(node))

    print(f'wrote output to {outpath}')


if __name__ == '__main__':
    main()
