
import pandas as pd
import matplotlib.pyplot as plt

from .trajectories import VARIABLE_LABELS


def plot_participant_comparison(
    df,
    variable,
    participant_ids=None,
    participant_col="participant_id",
    day_col="day",
    ax=None
):
    """
    Plot individual longitudinal trajectories and their
    observed group mean.

    Missing observations are retained as gaps.
    """

    required = [participant_col, day_col, variable]
    missing = [c for c in required if c not in df.columns]

    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    data = df.copy()

    if participant_ids is not None:
        data = data.loc[
            data[participant_col].isin(participant_ids)
        ]

    if data.empty:
        raise ValueError("No matching participant data found.")

    if data.duplicated([participant_col, day_col]).any():
        raise ValueError(
            "Duplicate participant-day observations detected."
        )

    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 5))

    # Complete day axis so absent days remain gaps
    all_days = sorted(data[day_col].dropna().unique())

    for participant, group in data.groupby(participant_col):

        trajectory = (
            group.set_index(day_col)[variable]
            .reindex(all_days)
        )

        ax.plot(
            all_days,
            trajectory,
            linewidth=1,
            alpha=0.45,
            label=str(participant)
        )

    # Mean calculated from available observations
    group_mean = (
        data.groupby(day_col)[variable]
        .mean()
        .reindex(all_days)
    )

    ax.plot(
        all_days,
        group_mean,
        color="black",
        linewidth=3,
        label="Observed group mean"
    )

    ax.set_xlabel("Study day")
    ax.set_ylabel(
        VARIABLE_LABELS.get(variable, variable)
    )
    ax.set_title(
        "Individual trajectories and group mean"
    )
    ax.legend()
    ax.grid(alpha=0.2)

    return ax
