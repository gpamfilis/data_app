import shutil
import datetime
from urllib.request import URLopener
import dateutil.relativedelta
import pandas as pd
import os
# from utilities import *

__author__ = 'gpamfilis'
__version__ = '1.0'
__contact__ = 'gpamfilis@gmail.com'


url_seed = "http://penteli.meteo.gr/meteosearch/data/"
data_folder = 'data'

'''
must change the location referring to for example "crete"
while the location referring to a location. now its mixed up.
'''


class MeteorologicalDataDownloader:
    """
    This is the meteorological data downloader class used to download data from the meteo.gr website.
    to run simply type the following:

    >>> mdd = MeteorologicalDataDownloader()
    >>> mdd.main()

    Thats it!!

    to set the year limits simply type (before the mdd.main()):
    >>>mdd.year_from = 2000
    >>>mdd.year_to = 2016

    to set the location (crete, etc):
    >>> mdd.location = 'crete'
    """

    def __init__(self, year_from=2014, year_to=2015, location='crete'):
        self.year_from = year_from
        self.year_to = year_to
        self.dates_to_download = []
        self.location = location
        self.stations = pd.read_csv('locations/'+self.location+'.txt')  # in this location there are stations

    def dates_for_program(self):
        """
        this method will create a dates.txt file where the year and month will
        be stored from now to then. in a year-month format.
        """
        years = self.year_to - self.year_from  # number of years between now and then
        for i in range(years*12):
            now = datetime.datetime.now()
            before = now + dateutil.relativedelta.relativedelta(months=-i)
            self.dates_to_download.append(str(before)[0:7])
        return self.dates_to_download

    def download_file(self):
        """
        this function will visit a url for a specific location, enter the date
        and save the file to a specified directory
        # http://penteli.meteo.gr/meteosearch/data/aghiosnikolaos/2009-11.txt
        """
        for station in self.stations['stations'][:]:
            try:
                os.mkdir('./data/'+station)
                # os.mkdir(os.path.join(os.getcwd(), data_folder)+'/'+station)  # messy!!!
            except:
                # add logging and fix exceptions too broad
                print('directory: {0} all ready exists!!!'.format(station))
                pass
            testfile = URLopener()
            # os.chdir(data_folder + '/' + station)
            for i, date in enumerate(self.dates_to_download):
                # name_to_save_file = os.getcwd() + '/' + station + '-' + date + '.txt'
                # print(os.getcwd())
                try:
                    #  this is the complete url to visit and download its contents
                    url = url_seed + station + '/' + date + '.txt'
                    testfile.retrieve(url, './data/' + station + '/' + station + '-' + date + '.txt')
                except:
                    pass
            # os.chdir(os.pardir)
            # os.chdir(os.pardir)

    def main(self):
        if not os.path.exists(data_folder):
            os.makedirs(data_folder)
        else:
            shutil.rmtree(data_folder)
            os.makedirs(data_folder)
        self.dates_for_program()
        self.download_file()

if __name__ == "__main__":
    mdd = MeteorologicalDataDownloader(2014, 2015, location='crete')
    mdd.main()


# bibliography:
# http://stackoverflow.com/questions/273192/in-python-check-if-a-directory-exists-and-create-it-if-necessary
# http://stackoverflow.com/questions/303200/how-do-i-remove-delete-a-folder-that-is-not-empty-with-python











