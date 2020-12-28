import os
import re
from datetime import datetime

import click

from utils import create_connection, wipe_table


def get_centered_text(text: str):
    pad = int(click.termui.get_terminal_size()[0] - len(text)) // 2
    formatted_text = "".join([" " for pix in range(pad)])

    formatted_text += text

    return formatted_text


def get_symbols():
    terminal_width = int(click.termui.get_terminal_size()[0])
    return "".join(["=" for i in range(terminal_width)])


def display_intro():
    click.secho(f"""
        Terminal Notes ~ Saakshaat
    """, fg='blue')
    click.secho(get_symbols(), fg='green')
    click.secho(f"""
        {get_centered_text("Take notes directly from your terminal.")}
        {get_centered_text("Notes CLI allows you to save notes locally in a SQLite database which is cached to a memory threshold of 50 notes.")}
        {get_centered_text("With Notes CLI, you can save your ToDos, meeting notes and much more conveniently and quickly.")}
                """, fg='red')
    click.secho(get_symbols(), fg='green')

    return None


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


@cli.command(help='Add note to memory.', name='add')
# @click.argument("profile", required=False, type=click.Choice(get_all_profiles()))
@click.argument('content', nargs=-1)
@click.option('-e', '--editor', is_flag=True,
              help='Write your notes in vim. Super useful for longer notes.')
@click.pass_context
def add(ctx, editor, content):
    if editor:
        content = click.edit("Complete your note below:\n")
        content = content.replace('\n', ' ')

    conn = ctx.obj['conn']
    conn.execute(
        f"""
        INSERT INTO notes (content, created_at) VALUES ('{content}', '{datetime.now().strftime("%H:%M ~ %d %b %Y")}');
        """
    )
    conn.commit()


@cli.command(name='delete', help='Remove note(s) from memory.')
# @click.argument("profile", required=False, type=click.Choice(get_all_profiles()))
@click.option('--date', '-d', type=str, help='Look for note to delete by date')
@click.option('--content', '-c', type=str, help='Look for note to delete by content')
@click.pass_context
def delete(ctx, date, content):
    conn = ctx.obj['conn']
    if not date and not content:
        click.secho('Must provide either date or content to match note.', bg='red')
    if date:
        conn.execute(
            f"""
                DELETE notes WHERE notes.created_at LIKE '%{date}%');
            """
        )
    elif content:
        conn.execute(
            f"""
                        DELETE FROM notes WHERE notes.content LIKE '%{content}%');
                    """
        )

    conn.commit()
    show(obj={})


@cli.command(help='Wipe all notes from memory', name='wipe')
# @click.argument("profile", required=False, type=click.Choice(get_all_profiles()))
@click.pass_context
def wipe(ctx):
    wipe_table(ctx.obj["conn"])
    click.echo("MEMORY WIPED SUCCESSFULLY 🧼")
