from flask import Flask

daily_indemnity_by_hour = 0.4015
hour_cost_brut = 4.36
hour_per_week = 32
weeks_by_year = 52
percent_cotisations = 0.78

csv_name = "historique.csv"

app = Flask(__name__)