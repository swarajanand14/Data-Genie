import matplotlib.pyplot as plt

def customize_chart(ax, title=None, xlabel=None, ylabel=None, legend=True):
    """Customize a Matplotlib chart with common options."""
    if title:
        ax.set_title(title, fontsize=14, fontweight="bold")
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=12)
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=12)
    if legend:
        ax.legend()
    ax.grid(True, linestyle="--", alpha=0.6)