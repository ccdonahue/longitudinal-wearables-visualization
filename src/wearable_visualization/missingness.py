
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch


def plot_missingness_heatmap(
    df,
    variable,
    participant_col="participant_id",
    day_col="day",
    expected_days=None,
    ax=None
):
    """
    Plot participant-by-day data availability.

    Observed values are coded as 1.
    Missing values or absent participant-day rows are coded as 0.

    Parameters
    ----------
    df : pandas.DataFrame
        Longitudinal wearable observations.
    variable : str
        Measurement to examine.
    participant_col : str
        Participant identifier column.
    day_col : str
        Study-day column.
    expected_days : iterable, optional
        Complete expected day sequence.
    ax : matplotlib.axes.Axes, optional
        Existing axes.

    Returns
    -------
    matplotlib.axes.Axes
        Axes containing the heatmap.
    """

    required = [participant_col, day_col, variable]
    missing = [c for c in required if c not in df.columns]

    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    if df.empty:
        raise ValueError("Input dataset is empty.")

    if df.duplicated([participant_col, day_col]).any():
        raise ValueError(
            "Duplicate participant-day observations detected."
        )

    participants = sorted(df[participant_col].dropna().unique())

    if expected_days is None:
        days = sorted(df[day_col].dropna().unique())
    else:
        days = list(expected_days)

    if not participants or not days:
        raise ValueError("No valid participants or days found.")

    if len(set(days)) != len(days):
        raise ValueError("Expected days must be unique.")

    # Construct the complete participant-by-day grid.
    availability = (
        df.assign(observed=df[variable].notna().astype(int))
        .pivot(
            index=participant_col,
            columns=day_col,
            values="observed"
        )
        .reindex(index=participants, columns=days)
        .fillna(0)
        .astype(int)
    )

    if ax is None:
        fig, ax = plt.subplots(figsize=(12, 6))

    cmap = ListedColormap(["#f59e0b", "#2563eb"])

    ax.imshow(
        availability.to_numpy(),
        aspect="auto",
        interpolation="nearest",
        cmap=cmap,
        vmin=0,
        vmax=1
    )

    ax.set_yticks(np.arange(len(participants)))
    ax.set_yticklabels(participants)

    ax.set_xticks(np.arange(len(days)))
    ax.set_xticklabels(days, rotation=90)

    ax.set_xlabel("Study day")
    ax.set_ylabel("Participant")
    ax.set_title(f"Data availability: {variable}")

    ax.legend(
        handles=[
            Patch(facecolor="#2563eb", label="Observed"),
            Patch(facecolor="#f59e0b", label="Missing")
        ],
        loc="upper left",
        bbox_to_anchor=(1.01, 1)
    )

    return ax
