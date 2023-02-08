from app import app
import views
from blueprint import data_csv_api

app.register_blueprint(data_csv_api, url_prefix='/data_csv')

if __name__ == "__main__":
    app.run()