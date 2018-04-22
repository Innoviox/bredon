from controller import *
import click

def validate_type(ctx, param, value):
    t, *n = value.split(":")
    t = t.upper()
    if t == "HUMAN":
        return HUMAN
    elif t == "AI":
        try:
            return AI(int(n[0]))
        except ValueError:
            raise click.BadParameter("depth must be a valid integer")
    else:
        raise click.BadParameter("type must be either 'human' or 'ai'")

def validate_game(ctx, param, value):
    try:
        return globals()[value]
    except KeyError:
        raise click.BadParameter("must be TextGame or ViewGame")

@click.command()
@click.argument("game", callback=validate_game)
@click.option("--size", default=5, help="The size of the board")
@click.option("--white", default="human", callback=validate_type,
              help="Type of the white player, type:depth")
@click.option("--black", default="ai:3", callback=validate_type,
              help="Type of the black player, type:depth")
def run_game(game, size, white, black):
    game(size=size, white=white, black=black).run()

if __name__ == '__main__':
    run_game()