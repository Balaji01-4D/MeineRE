import click
from .app import run
from .utils.file_manager import Quotes, clear_history

@click.command()
@click.option('--quotes.reset', 'quotes_reset', is_flag=True, help='Reset quotes file to default.')
@click.option('--quotes.clear', 'quotes_clear', is_flag=True, help='Clear all user quotes.')
@click.option('--quotes.add', 'quote_to_add', help='Add a new quote string to user quotes.')
@click.option('--history.clear','history_clear', is_flag=True,help='Clear the Input history')
def main(quotes_reset, quotes_clear, quote_to_add, history_clear):
    quotes = Quotes()

    used_flags = sum(map(bool, [quotes_reset, quotes_clear, quote_to_add]))
    if used_flags > 1:
        click.echo("Error: Use only one --quotes option at a time.", err=True)
        return

    if quotes_reset:
        quotes.reset()
        click.echo("Quotes reset to default.")

    elif quotes_clear:
        quotes.clear()
        click.echo("Quotes cleared.")

    elif quote_to_add:
        quotes.add_quote(quote_to_add)
        click.echo(f"Quote added: {quote_to_add}")

    elif history_clear:
        clear_history()
        click.echo('Hisoty cleared')


    else:
        run()

if __name__ == '__main__':
    main()
