"""Command line interface for venomx."""

import logging

import click

__all__ = [
    "main",
]

from venomx.tools.file_io import EmbeddingFormat, load_index, save_index

logger = logging.getLogger(__name__)


input_embeddings_format_option = click.option(
    "-f",
    "--input-embeddings-format",
    type=click.Choice([x.value for x in EmbeddingFormat]),
    default="parquet",
    help="Format of the input embeddings.",
)
output_embeddings_format_option = click.option(
    "-t",
    "--output-embeddings-format",
    type=click.Choice([x.value for x in EmbeddingFormat]),
    default="parquet",
    help="Format of the output embeddings.",
)
output_option = click.option(
    "-o",
    "--output",
    required=True,
    type=click.Path(),
    help="Output path.",
)


@click.group()
@click.option("-v", "--verbose", count=True)
@click.option("-q", "--quiet")
def main(verbose: int, quiet: bool):
    """
    CLI for venomx.

    :param verbose: Verbosity while running.
    :param quiet: Boolean to be quiet or verbose.
    """
    if verbose >= 2:
        logger.setLevel(level=logging.DEBUG)
    elif verbose == 1:
        logger.setLevel(level=logging.INFO)
    else:
        logger.setLevel(level=logging.WARNING)
    if quiet:
        logger.setLevel(level=logging.ERROR)


@main.command()
@input_embeddings_format_option
@click.argument("input_file")
def validate(input_file: str, input_embeddings_format: str):
    """Validate an index."""
    load_index(input_file, format=input_embeddings_format, check=True)


@main.command()
@click.argument("input_file")
@input_embeddings_format_option
@output_embeddings_format_option
@output_option
def convert(input_file: str, input_embeddings_format: str, output_embeddings_format: str, output: str):
    """Merge an index."""
    ix = load_index(input_file, format=EmbeddingFormat(input_embeddings_format), check=True)
    save_index(ix, output, format=EmbeddingFormat(output_embeddings_format))


@main.command()
@click.argument("input_file")
def info(input_file: str):
    """Show information."""
    ix = load_index(input_file, check=True)
    print(f"Num objects: {len(ix.objects)}")


if __name__ == "__main__":
    main()
