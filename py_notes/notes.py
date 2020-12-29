import os
import re
from datetime import datetime

import click

from .utils.db import create_connection, wipe_table


def get_symbols():
    # we need to use a constant value for the ``terminal_width`` since Click's `help` window set's constraints
    # on the width used for the help prompt and the symbols would overflow if the window gets wider
    terminal_width = 36
    return "".join(["=" for pix in range(terminal_width)])


def display_intro():
    cli_name = click.style("Terminal Notes ~ Saakshaat", fg='blue')
    cli_bars = click.style(get_symbols(), fg='green')
    cli_description = click.style(f"""
       {"Take notes directly from your terminal."}

        {"Notes CLI allows you to save notes locally in a SQLite database which is cached to a memory threshold of 25 notes."}

        {"With Notes CLI, you can save your ToDos, meeting notes and much more conveniently and quickly."}""",
                                  fg='red')

    full_intro = f"""{cli_name}\n
{cli_bars}\n
{cli_description}\n
{cli_bars}\n
    """

    return full_intro


def get_all_profiles():
    db_files = [f for f in os.listdir(os.path.realpath(f'{__file__}/../../utils/databases/')) if
                re.match(r'.*\.sqlite3', f)]
    profile_names = [file.split('.')[0] for file in db_files]
    if not profile_names:
        profile_names.append('general')
    return profile_names


@click.group(help=display_intro())
@click.pass_context
def cli(ctx):
    click.style("", fg='white')
    ctx.ensure_object(dict)

    conn, cur = create_connection()

    ctx.obj['conn'] = conn
    ctx.obj['cur'] = cur


# @cli.command(help="Configure profile with it's own notes.", name='profile')
# @click.option('--add', '-a', 'action', flag_value='add',
#               default=True)
# @click.option('--delete', '-d', 'action', flag_value='delete')
# @click.pass_context
# def profile(ctx, profile, action):
#     if action == 'add':
#         create_connection(profile)
#         click.secho(f"Profile {profile} created!", fg='green')
#     else:
#         click.secho(f"Profile {profile} deleted!", fg='blue')


@cli.command(help='Show notes by params.', name='show')
# @click.argument("profile", required=False, type=click.Choice(get_all_profiles()))
@click.option('--search', '-s', help='Search for a note by substring.')
@click.pass_context
def show(ctx, search):
    query_with_param = f"SELECT created_at, content FROM notes WHERE notes.content LIKE '%{search}%';"
    query_without_param = f"SELECT created_at, content FROM notes"
    curs = ctx.obj['conn'].execute(query_with_param if search else query_without_param)

    row = curs.fetchone()

    click.echo("       Date         |         Content")
    click.echo("--------------------|--------------------")
    while row:
        click.echo("{} | {}".format(row[0], row[1]))
        row = curs.fetchone()


def reorganize_memory(conn):
    query = conn.execute("SELECT COUNT(*) FROM notes;")
    count = int(query.fetchone()[0])

    if count >= 25:
        click.secho(f"Memory Full. Deleted note: \n{conn.execute('SELECT created_at, content FROM notes;').fetchone()[1]}",
                    fg='green')
        conn.execute("DELETE FROM notes WHERE id = (SELECT MIN(id) FROM notes);")


@cli.command(help='Add note to memory.', name='add')
# @click.argument("profile", required=False, type=click.Choice(get_all_profiles()))
@click.argument('content', required=False)
@click.option('-e', '--editor', is_flag=True,
              help='Write your notes in vim. Super useful for longer notes.')
@click.pass_context
def add(ctx, editor, content):
    if editor:
        content = click.edit("Complete your note below:\n")
        content = content.replace('\n', ' ')

    conn = ctx.obj['conn']

    reorganize_memory(conn)

    conn.execute(
        f"""
            INSERT INTO notes (content, created_at) VALUES ('{content}', '{datetime.now().strftime("%H:%M ~ %d %b %Y")}');
        """
    )
    conn.commit()


@cli.command(help='Remove note(s) from memory.', name='delete')
# @click.argument("profile", required=False, type=click.Choice(get_all_profiles()))
@click.option('--content', '-c', type=str, required=False, help='Look for note to delete by content')
@click.option('--date', '-d', type=str, required=False, help='Look for note to delete by date')
@click.pass_context
def delete(ctx, date, content):
    conn = ctx.obj['conn']
    if not date and not content:
        click.secho('Must provide either date or content to match note.', bg='red')
    if date and content:
        conn.execute(
            f"""
                    DELETE FROM notes WHERE notes.created_at LIKE '%{date}%' AND notes.content LIKE '%{content}%';
            """
        )
    elif date:
        conn.execute(
            f"""
                DELETE FROM notes WHERE notes.created_at LIKE '%{date}%';
            """
        )
    elif content:
        conn.execute(
            f"""
                DELETE FROM notes WHERE CONTENT LIKE '%{content}%';
            """
        )

    conn.commit()


@cli.command(help='Wipe all notes from memory', name='wipe')
# @click.argument("profile", required=False, type=click.Choice(get_all_profiles()))
@click.pass_context
def wipe(ctx):
    click.confirm("Are you sure you want to delete all notes? This cannot be undone.", abort=True)
    wipe_table(ctx.obj["conn"])
    click.echo("MEMORY WIPED SUCCESSFULLY 🧼")
