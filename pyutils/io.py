#description


# imports



def generate_lines(f: io.FileIO, max_bytes: int = 1_073_741_824) -> Iterator[str]:
    """
    Lazily generates lines from a file.

    :param f:
        The opened file from which to generate lines.
    :param max_bytes:
        The maximum number of bytes worth of a batch of whole lines that will be read into memory at a time.
        Default value is 1 GiB.
    :return:
        A lazy iterator over lines in the file.
    """
    line = f.readline(max_bytes)
    while line:
        yield line
        line = f.readline(max_bytes)
