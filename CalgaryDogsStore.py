import pandas as pd
import numpy as np


class CalgaryDogStore:
    """
    Helper class for storing Calgary Dog data and printing stats against it.

    Attributes:
        data (pandas.DataFrame): Calgary Dog data
        breeds (list[str]) : list of breeds
        breeds_help (str) : stylized string of all breeds of dogs
        breed (str) : the name of the breed use for printing stats
    """
    data = pd.read_excel('Assets/CalgaryDogBreeds.xlsx')
    breeds : list[str] = data.Breed.unique()
    breeds_help: str = ',\n'.join([', '.join(x) for x in np.array(breeds).reshape(int(len(breeds) / 10), 10)])

    @staticmethod
    def is_breed_not_in_data(input_breed : str) -> bool :
        """
        Helper method to check if a breed is not in the data.
        :param input_breed: breed of dog
        :type input_breed : str
        :return: true if breed is not in the data, false otherwise
        """
        return input_breed not in CalgaryDogStore.breeds

    def __init__(self, breed: str):
        self.breed = breed

    def print_top_years(self):
        """
        print years for the input breed where it has among top number of registrations
        """
        print(f'The {self.breed} was found in the top breeds for years: {
        ' '.join(str(x) for x in CalgaryDogStore.data[CalgaryDogStore.data['Breed'] == self.breed].Year.unique())
        }')

    def print_total_registration(self):
        """
        print total registration for the input breed
        """
        print(f'There have been {
        CalgaryDogStore.data[CalgaryDogStore.data['Breed'] == self.breed].Total.sum()
        } {self.breed} dogs registered total.')

    def print_yearly_perc_registration(self):
        """
        print yearly registration for the input breed as a percentage of overall registrations for that year
        """
        for x in [2021, 2022, 2023]:
            year_total_data = CalgaryDogStore.data[CalgaryDogStore.data['Year'] == x]
            breed_total_data = year_total_data[year_total_data['Breed'] == self.breed]
            print(f'The {self.breed} was {
                breed_total_data.Total.sum() * 100 / year_total_data.Total.sum() : .6f}% of the top breeds in {x}')

    def print_total_perc_registration(self):
        """
        print total registrations for the input breed as a percentage of overall registrations in the data
        """
        all_year_data = CalgaryDogStore.data[CalgaryDogStore.data['Year'].isin(CalgaryDogStore.data['Year'].unique())]
        breed_all_year_data = all_year_data[all_year_data['Breed'] == self.breed]
        print(
            f'The {self.breed} was {breed_all_year_data.Total.sum() * 100 / all_year_data.Total.sum() : .6f}% of the top breed across all years.')

    def print_popular_months(self):
        """
        print months, where the input breed is the top breed registered
        """
        inter_mod = CalgaryDogStore.data.groupby(['Month', 'Breed'], as_index=False).agg({'Total': 'sum'})
        inter_mod_max = inter_mod.groupby('Month')['Total'].transform('max')
        print(
            f'Most popular month(s) for {self.breed} dogs: {
            ' '.join(inter_mod[(inter_mod['Total'] == inter_mod_max) & (inter_mod['Breed'] == self.breed)]['Month'].values)
            }')