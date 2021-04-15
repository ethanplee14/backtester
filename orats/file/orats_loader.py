from datetime import date, datetime
import pandas as pd
import os


class OratsLoader:

    _FILE_BASE = "ORATS_SMV_Strikes"

    def __init__(self, orats_dir: str, is_files_zipped=True):
        """
        Orats file loader
        Orats working directory. Should contain folders by year, which contains csv zip files by day
        :param orats_dir: Orats working directory string path
        """
        self.orats_dir = orats_dir
        self._day_df = None
        self.is_files_zipped = is_files_zipped

    def all_years(self):
        avail_years = {}
        for year in os.listdir(self.orats_dir):
            files = os.listdir(self.orats_dir + "/" + year)
            days = list(map(OratsLoader._parse_date, files))
            avail_years[year] = days
        return avail_years

    def all_days(self):
        days = []
        for year_days in self.all_years().values():
            for year_day in year_days:
                days.append(year_day)
        return days

    def load_day(self, data_date: date):
        dashless_date = str(data_date).replace('-', '')
        file_name = self._FILE_BASE + "_" + dashless_date
        file_path = f"{self.orats_dir}/{data_date.year}/{file_name}"
        if self.is_files_zipped:
            file_path += ".zip"
        else:
            file_path += f"/{file_name}.csv"

        self._day_df = pd.read_csv(file_path)
        return self._day_df

    def options_chain(self, symbol: str):
        if self._day_df is None:
            raise Exception("Load day file before getting options chain")

        return self._day_df.loc[self._day_df["ticker"] == symbol]

    def load_options_chain(self, symbol: str, data_date: date):
        self.load_day(data_date)
        return self.options_chain(symbol)

    def reset(self):
        self._day_df = None

    @staticmethod
    def _parse_date(file_name: str):
        file_name = file_name[:-4]
        return datetime.strptime(file_name.split('_')[-1], "%Y%m%d").date()


