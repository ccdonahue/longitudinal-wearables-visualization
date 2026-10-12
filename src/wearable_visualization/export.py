
from pathlib import Path
import matplotlib.pyplot as plt


def save_figure(
    fig,
    filename,
    output_dir="figures",
    dpi=300,
    formats=("png", "pdf")
):
    """
    Save a Matplotlib figure in one or more formats.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        Figure to save.
    filename : str
        Base filename without extension.
    output_dir : str or Path
        Destination folder.
    dpi : int
        Resolution for raster images.
    formats : tuple
        Output formats, such as PNG and PDF.

    Returns
    -------
    list
        Paths to saved files.
    """

    if not filename or Path(filename).name != filename:
        raise ValueError("Provide a simple filename.")

    if dpi <= 0:
        raise ValueError("DPI must be positive.")

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    saved_files = []

    for fmt in formats:

        if fmt not in ("png", "pdf"):
            raise ValueError(f"Unsupported format: {fmt}")

        output_path = output_dir / f"{filename}.{fmt}"

        fig.savefig(
            output_path,
            dpi=dpi,
            bbox_inches="tight",
            facecolor="white"
        )

        saved_files.append(output_path)

    return saved_files
