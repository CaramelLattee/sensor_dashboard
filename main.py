from data_loader     import DataLoader
from analyser        import Analyser
from chart_generator import ChartGenerator
import os

def main():
    print("=" * 50)
    print("  📊 SENSOR DASHBOARD GENERATOR v1.0")
    print("=" * 50)

    # ── Load Data ──
    loader = DataLoader(
        "sample_data/sensor_readings.csv")
    df = loader.load()

    if df is None:
        print("❌ Cannot load data!")
        return

    loader.get_summary()

    # ── Analyse Data ──
    analyser = Analyser(df)
    analyser.print_analysis()

    # ── Generate Charts ──
    print("\n--- GENERATING DASHBOARD ---")
    os.makedirs("output", exist_ok=True)

    charts = ChartGenerator(df, analyser)
    charts.generate_dashboard(
        "output/dashboard.png")

    print("\n✅ Complete!")
    print("📊 Open output/dashboard.png to view!")

if __name__ == "__main__":
    main()