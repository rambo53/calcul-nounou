from datetime import datetime
import time
from app import daily_indemnity_by_hour, hour_cost_brut, hour_per_week, weeks_by_year, percent_cotisations

class Tarif():


    def __init__(self, dateRegister, hourIn, hourOut):
        self.dateRegister = dateRegister
        self.hourIn = hourIn
        self.hourOut = hourOut
        self.month_cost_brut = round((hour_cost_brut*hour_per_week*weeks_by_year)/12, 2)


    def diffHour(day, hour):
        day_hour = datetime.strptime(day+'-'+hour,"%Y-%m-%d-%H:%M")
        tuple = day_hour.timetuple()
        timestamp = time.mktime(tuple)

        return datetime.fromtimestamp(timestamp)
        

    def hourCount(self):
        timestamp_in = Tarif.diffHour(self.dateRegister, self.hourIn)
        timestamp_out = Tarif.diffHour(self.dateRegister, self.hourOut)
        diff = timestamp_out - timestamp_in
        
        return diff


    def dailyIndemnity(self, hours):
        minutes_tab = str(hours).split(":")
        minutes_tab = [int(i) for i in minutes_tab]
        hour_to_minutes = minutes_tab[0]*60
        minutes_total = minutes_tab[1] + hour_to_minutes
        daily_indemnity = minutes_total/60*daily_indemnity_by_hour

        return round(daily_indemnity,2)
    
    def dailyCostHour(self, nb_hours):
        month_cost_net = self.month_cost_brut * percent_cotisations
        
