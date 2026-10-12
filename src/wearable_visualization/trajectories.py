
import pandas as pd
import matplotlib.pyplot as plt


VARIABLE_LABELS = {
    "sleep_duration_min": "Sleep duration (minutes)",
    "hrv_rmssd_ms": "HRV RMSSD (ms)",
    "steps": "Daily steps"
}


def plot_individual_trajectory(
    df,
    participant_id,
    variable,
    participant_col="participant_id",
    date_col="date",
    ax=None
):
    """
    Plot longitudinal observations for one participant.

    Missing values remain as gaps in the plotted line.

    Parameters
    ----------
    df : pandas.DataFrame
        Longitudinal wearable observations.
    participant_id : str
        Participant identifier.
    variable : str
        Measurement to visualize.
    participant_col : str
        Participant identifier column.
    date_col : str
        Date column.
    ax : matplotlib.axes.Axes, optional
        Existing axes on which to draw the figure.

    Returns
    -------
    matplotlib.axes.Axes
        Axes containing the trajectory.
    """

    required = [participant_col, date_col, variable]

    missing = [
        col for col in required
        if col not in df.columns
    ]

    if missing:
        raise ValueError(
            f"Missing required columns: {missing}"
        )

    participant_data = df.loc[
        df[participant_col] == participant_id
    ].copy()

    if participant_data.empty:
        raise ValueError(
            f"Participant {participant_id} not found."
        )

    participant_data[date_col] = pd.to_datetime(
        participant_data[date_col]
    )

    participant_data = participant_data.sort_values(
        date_col
    )

    if participant_data[date_col].duplicated().any():
        raise ValueError(
            "Duplicate dates detected for participant."
        )

    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 4))

    ax.plot(
        participant_data[date_col],
        participant_data[variable],
        marker="o",
        linewidth=1.5,
        markersize=4
    )

    ax.set_title(
        f"{participant_id}: {variable.replace('_', ' ').title()}"
    )

    ax.set_xlabel("Date")

    ax.set_ylabel(
        VARIABLE_LABELS.get(
            variable,
            variable.replace("_", " ").title()
        )
    )

    ax.grid(alpha=0.25)

    return ax
