#data_loader.py

import pandas as pd
import os

class DataLoader:
    """Loads and validates sensor CSV data"""

    def __init__(self, filepath):
        self.filepath = filepath
        self.df       = None

    def load(self):
        """Load CSV into pandas DataFrame"""
        try:
            if not os.path.exists(self.filepath):
                raise FileNotFoundError(
                    f"File not found: {self.filepath}")

            self.df = pd.read_csv(self.filepath)
            self.df["Timestamp"] = pd.to_datetime(
                                   self.df["Timestamp"])

            print(f"✅ Loaded {len(self.df)} readings")
            print(f"   Columns: {list(self.df.columns)}")
            return self.df

        except FileNotFoundError as e:
            print(f"❌ {e}")
            return None
        except Exception as e:
            print(f"❌ Load error: {e}")
            return None

    def get_summary(self):
        """Print basic data summary"""
        if self.df is None:
            return

        print("\n--- DATA SUMMARY ---")
        print(f"Total readings : {len(self.df)}")
        print(f"Time range     : "
              f"{self.df['Timestamp'].min()} → "
              f"{self.df['Timestamp'].max()}")
        print(f"Pass count     : "
              f"{(self.df['Status']=='PASS').sum()}")
        print(f"Fail count     : "
              f"{(self.df['Status']=='FAIL').sum()}")