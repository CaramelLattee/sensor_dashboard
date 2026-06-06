# Sensor Dashboard

A Python data analytics dashboard that reads sensor CSV data and generates professional matplotlib charts for engineering analysis.

## Features

- Voltage and Current trend lines with spec limits
- Pass/Fail distribution pie chart
- FPY First Pass Yield bar chart
- Temperature and Pressure histograms
- Statistics summary table
- Professional dark theme dashboard
- Exports to PNG image

## Tech Stack

- Python 3.12+
- Pandas for data loading and analysis
- Matplotlib for chart generation
- NumPy for numerical calculations
- OOP with 4 separate modules

## How To Run

Install dependencies first:
pip install matplotlib pandas numpy

Generate sample data:
cd sample_data
python generate_data.py
cd ..

Run dashboard:
python main.py

## Dashboard Preview

![Dashboard](dashboard.png)

## Spec Limits

Voltage   : 4.5V - 5.5V
Current   : 0.8A - 1.2A
Temperature: 20C - 35C
Pressure  : 2.0bar - 4.0bar

## Author

Muhammad Hafizul Bin Ahmad Husni
Mechatronics Engineering USM