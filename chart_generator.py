import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np

class ChartGenerator:
    """Generates sensor analysis charts"""

    def __init__(self, df, analyser):
        self.df       = df
        self.analyser = analyser

    def generate_dashboard(self, output_path):
        """Generate full dashboard image"""

        # Create figure with grid layout
        fig = plt.figure(figsize=(16, 12))
        fig.patch.set_facecolor('#1a1a2e')

        gs = gridspec.GridSpec(3, 3,
                               figure=fig,
                               hspace=0.4,
                               wspace=0.35)

        # Title
        fig.suptitle(
            "⚙️  SENSOR MONITORING DASHBOARD\n"
            "Company A",
            fontsize=14, fontweight='bold',
            color='white', y=0.98)

        # ── Chart 1: Voltage Trend ──
        ax1 = fig.add_subplot(gs[0, :2])
        self._plot_trend(ax1, "Voltage", "V",
                         4.5, 5.5, "#00c8ff")

        # ── Chart 2: Pass/Fail Pie ──
        ax2 = fig.add_subplot(gs[0, 2])
        self._plot_pie(ax2)

        # ── Chart 3: Current Trend ──
        ax3 = fig.add_subplot(gs[1, :2])
        self._plot_trend(ax3, "Current", "A",
                         0.8, 1.2, "#00ff9d")

        # ── Chart 4: FPY Gauge ──
        ax4 = fig.add_subplot(gs[1, 2])
        self._plot_fpy(ax4)

        # ── Chart 5: Temperature ──
        ax5 = fig.add_subplot(gs[2, 0])
        self._plot_histogram(ax5, "Temperature",
                             "°C", 20, 35, "#ffd700")

        # ── Chart 6: Pressure ──
        ax6 = fig.add_subplot(gs[2, 1])
        self._plot_histogram(ax6, "Pressure",
                             "bar", 2.0, 4.0, "#ff6b35")

        # ── Chart 7: Stats Table ──
        ax7 = fig.add_subplot(gs[2, 2])
        self._plot_stats_table(ax7)

        plt.savefig(output_path,
                    dpi=150,
                    bbox_inches='tight',
                    facecolor='#1a1a2e')
        plt.close()
        print(f"✅ Dashboard saved: {output_path}")

    def _plot_trend(self, ax, column, unit,
                    lsl, usl, color):
        """Plot sensor trend line"""
        ax.set_facecolor('#0d1829')
        ax.plot(self.df.index,
                self.df[column],
                color=color, linewidth=1,
                alpha=0.8, label=column)

        # Spec limit lines
        ax.axhline(y=lsl, color='red',
                   linestyle='--',
                   alpha=0.7, label=f'LSL={lsl}')
        ax.axhline(y=usl, color='red',
                   linestyle='--',
                   alpha=0.7, label=f'USL={usl}')

        # Fill spec zone
        ax.axhspan(lsl, usl, alpha=0.1,
                   color='green')

        ax.set_title(f"{column} Trend",
                     color='white', fontsize=10)
        ax.set_ylabel(f"{column} ({unit})",
                      color='white', fontsize=8)
        ax.tick_params(colors='white', labelsize=7)
        ax.legend(fontsize=7,
                  facecolor='#0d1829',
                  labelcolor='white')
        for spine in ax.spines.values():
            spine.set_color('#1a3a5c')

    def _plot_pie(self, ax):
        """Plot pass/fail distribution"""
        ax.set_facecolor('#0d1829')
        passed = (self.df["Status"]=="PASS").sum()
        failed = (self.df["Status"]=="FAIL").sum()

        colors  = ['#00ff9d', '#ff4444']
        explode = (0.05, 0.05)

        ax.pie([passed, failed],
               labels=['PASS', 'FAIL'],
               colors=colors,
               explode=explode,
               autopct='%1.1f%%',
               textprops={'color': 'white',
                          'fontsize': 9})
        ax.set_title("Pass/Fail Distribution",
                     color='white', fontsize=10)

    def _plot_fpy(self, ax):
        """Plot FPY as bar"""
        ax.set_facecolor('#0d1829')
        fpy = self.analyser.get_fpy()

        color = '#00ff9d' if fpy >= 95 else \
                '#ffd700' if fpy >= 80 else \
                '#ff4444'

        bars = ax.bar(['FPY'], [fpy],
                      color=color, width=0.4)
        ax.set_ylim(0, 110)
        ax.axhline(y=95, color='white',
                   linestyle='--',
                   alpha=0.5, label='Target 95%')
        ax.text(0, fpy + 2, f'{fpy}%',
                ha='center', color='white',
                fontweight='bold', fontsize=12)
        ax.set_title("First Pass Yield",
                     color='white', fontsize=10)
        ax.tick_params(colors='white', labelsize=8)
        ax.legend(fontsize=7,
                  facecolor='#0d1829',
                  labelcolor='white')
        for spine in ax.spines.values():
            spine.set_color('#1a3a5c')

    def _plot_histogram(self, ax, column,
                        unit, lsl, usl, color):
        """Plot histogram with spec limits"""
        ax.set_facecolor('#0d1829')
        ax.hist(self.df[column], bins=20,
                color=color, alpha=0.7,
                edgecolor='white',
                linewidth=0.5)

        ax.axvline(x=lsl, color='red',
                   linestyle='--',
                   alpha=0.8, label=f'LSL={lsl}')
        ax.axvline(x=usl, color='red',
                   linestyle='--',
                   alpha=0.8, label=f'USL={usl}')

        ax.set_title(f"{column} Distribution",
                     color='white', fontsize=10)
        ax.set_xlabel(f"{unit}",
                      color='white', fontsize=8)
        ax.tick_params(colors='white', labelsize=7)
        ax.legend(fontsize=7,
                  facecolor='#0d1829',
                  labelcolor='white')
        for spine in ax.spines.values():
            spine.set_color('#1a3a5c')

    def _plot_stats_table(self, ax):
        """Plot statistics table"""
        ax.set_facecolor('#0d1829')
        ax.axis('off')

        sensors = ["Voltage", "Current",
                   "Temperature", "Pressure"]
        col_labels = ['Sensor', 'Mean',
                      'Min', 'Max', 'Pass%']
        rows = []

        for s in sensors:
            stats = self.analyser.get_stats(s)
            pass_rate = stats.get('pass_rate', '-')
            rows.append([
                s[:4],
                f"{stats['mean']}",
                f"{stats['min']}",
                f"{stats['max']}",
                f"{pass_rate}%"
                if pass_rate != '-' else '-'
            ])

        table = ax.table(
            cellText=rows,
            colLabels=col_labels,
            loc='center',
            cellLoc='center'
        )
        table.auto_set_font_size(False)
        table.set_fontsize(7)
        table.scale(1, 1.5)

        # Style table
        for (row, col), cell in table.get_celld().items():
            cell.set_facecolor(
                '#1a3a5c' if row == 0 else '#0d1829')
            cell.set_text_props(color='white')
            cell.set_edgecolor('#1a3a5c')

        ax.set_title("Statistics Summary",
                     color='white', fontsize=10)