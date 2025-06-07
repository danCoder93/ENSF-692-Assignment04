import pandas as pd
import numpy as np
import math


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
        perc_yearly_total = (
                CalgaryDogStore.data[CalgaryDogStore.data['Breed'] == self.breed]
                .groupby('Year')['Total'].sum()
                * 100 /
                CalgaryDogStore.data.groupby('Year')['Total'].sum()
        )

        [
            print(f'The {self.breed} was {v 
            : .6f}% of the top breeds in {i}')
            for i, v in zip(perc_yearly_total.index, perc_yearly_total.values)
        ]

    def print_total_perc_registration(self):
        """
        print total registrations for the input breed as a percentage of overall registrations in the data
        """
        print(
            f'The {self.breed} was {
            CalgaryDogStore.data[CalgaryDogStore.data['Breed'] == self.breed].Total.sum() * 100 
            / CalgaryDogStore.data.Total.sum()
            : .6f}% of the top breed across all years.')

    def print_popular_months(self):
        """
        print months for input breed, where the input breed is top breed registered
        """

        months_sum = (CalgaryDogStore.data[CalgaryDogStore.data['Breed'] == self.breed]
                      .groupby('Month', as_index=False).agg({'Total': 'sum'}))
        months_sum_max = months_sum['Total'].max()
        log_10_power : int = int(math.log10(months_sum_max))
        log_10_multiplier: int = int(months_sum_max/ 10**log_10_power)
        max_threshold : int = log_10_multiplier * (10**log_10_power)

        print(
            f'Most popular month(s) for {self.breed} dogs: {
            ' '.join(months_sum[months_sum['Total'] > max_threshold]['Month'].unique())
            }')