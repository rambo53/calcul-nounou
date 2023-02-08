import pandas as pd
from app import csv_name

class DataCsv():

    def __init__(self):
        self.df_historique = pd.read_csv(csv_name, sep=";")


    def checkDateExist(self, date):
        date_exist = self.df_historique[self.df_historique["date"] == date]
        if not date_exist.empty:
            raise Exception(f"La date :{date}, est déjà enregistrée.")


    def post_data(self, data, nb_hours, daily_indemnity):

        fake_cout_heure = 18

        df_to_add = pd.DataFrame()

        lst_val = [
            data['dateRegister'][:-3],
            data['dateRegister'],
            data['hourIn'],
            data['hourOut'],
            str(nb_hours).split(" ")[0],
            fake_cout_heure,
            daily_indemnity,
            round(fake_cout_heure+daily_indemnity,2)
        ]

        for i, col in enumerate(self.df_historique.columns):
            df_to_add[col] = [lst_val[i]]

        self.df_historique = pd.concat([self.df_historique, df_to_add],ignore_index=True)
        self.df_historique.to_csv(csv_name, sep=";", index=False)


    def getDetails(self, year_month):
        df = self.df_historique[self.df_historique["mois_annee"] == year_month]
        if df.empty:
            raise Exception(f"Il n'y a pas de données pour {year_month}.")
        df["date"] = df["date"].astype('datetime64[ns]')

        return df.sort_values(by='date', ignore_index=True)

    
    def get_hours_month(self, df_month):
        df_month['nb_heures'] = pd.to_timedelta(df_month.nb_heures)
        total_time_delta = str(df_month['nb_heures'].sum())
        day_hour_min = total_time_delta.split(" ")
        days_to_hour = int(day_hour_min[0])*24
        hour_min = day_hour_min[2].split(":")
        total_hour = int(hour_min[0]) + days_to_hour

        return f"{total_hour}h {hour_min[1]}min"

    
    def get_total_cost_month(self, df_month):
        return round(df_month["total_jour"].sum(),2)


    def updateData(self, data, nb_hours, daily_indemnity):
        fake_cout_heure = 18

        id = self.df_historique.index[self.df_historique["date"] == data['dateRegister']][0]

        self.df_historique.at[id,'heure_arrive'] = data['hourIn']
        self.df_historique.at[id,'heure_depart'] = data['hourOut']
        self.df_historique.at[id,'nb_heures'] = nb_hours
        self.df_historique.at[id,'cout_heure'] = fake_cout_heure
        self.df_historique.at[id,'cout_indemnite'] = daily_indemnity
        self.df_historique.at[id,'total_jour'] = round(fake_cout_heure+daily_indemnity,2)

        self.df_historique.to_csv(csv_name, sep=";", index=False)


    def deleteData(self, data):
        id = self.df_historique.index[self.df_historique["date"] == data['dateRegister']][0]
        self.df_historique = self.df_historique.drop(id)
        self.df_historique.to_csv(csv_name, sep=";", index=False)
        

            
       
