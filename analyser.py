#analyser.py
class Analyser:
    """Analyses sensor data"""

    # Spec limits
    LIMITS = {
        "Voltage"    : (4.5, 5.5),
        "Current"    : (0.8, 1.2),
        "Temperature": (20.0, 35.0),
        "Pressure"   : (2.0, 4.0)
    }

    def __init__(self, df):
        self.df = df

    def get_stats(self, column):
        """Get statistics for a column"""
        data = self.df[column]
        lsl, usl = self.LIMITS.get(
                   column, (None, None))

        stats = {
            "mean"   : round(data.mean(), 3),
            "std"    : round(data.std(),  3),
            "min"    : round(data.min(),  3),
            "max"    : round(data.max(),  3),
            "lsl"    : lsl,
            "usl"    : usl,
        }

        if lsl and usl:
            in_spec = data.between(lsl, usl)
            stats["pass_rate"] = round(
                in_spec.mean() * 100, 1)
            stats["fail_count"] = (~in_spec).sum()

        return stats

    def get_fpy(self):
        """Calculate overall FPY"""
        passed = (self.df["Status"] == "PASS").sum()
        total  = len(self.df)
        return round(passed / total * 100, 1)

    def get_fail_analysis(self):
        """Analyse failure patterns"""
        fails = self.df[self.df["Status"] == "FAIL"]
        return {
            "total_fails" : len(fails),
            "fail_rate"   : round(
                len(fails)/len(self.df)*100, 1),
            "volt_fails"  : len(fails[
                ~fails["Voltage"].between(4.5, 5.5)]),
            "curr_fails"  : len(fails[
                ~fails["Current"].between(0.8, 1.2)]),
        }

    def print_analysis(self):
        """Print full analysis"""
        print("\n" + "=" * 50)
        print("  SENSOR DATA ANALYSIS")
        print("=" * 50)

        sensors = ["Voltage", "Current",
                   "Temperature", "Pressure"]

        for sensor in sensors:
            stats = self.get_stats(sensor)
            print(f"\n{sensor}:")
            print(f"  Mean     : {stats['mean']}")
            print(f"  Std Dev  : {stats['std']}")
            print(f"  Min      : {stats['min']}")
            print(f"  Max      : {stats['max']}")
            if "pass_rate" in stats:
                print(f"  Pass Rate: {stats['pass_rate']}%")
                print(f"  Fails    : {stats['fail_count']}")

        fpy   = self.get_fpy()
        fails = self.get_fail_analysis()

        print(f"\n--- OVERALL ---")
        print(f"FPY          : {fpy}%")
        print(f"Total Fails  : {fails['total_fails']}")
        print(f"Volt Fails   : {fails['volt_fails']}")
        print(f"Curr Fails   : {fails['curr_fails']}")
        print("=" * 50)