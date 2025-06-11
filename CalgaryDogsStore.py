import pandas as pd
import numpy as np
import numpy.typing as npt
import math


class CalgaryDogStore:
    """
    Helper class for storing Calgary Dog data and printing stats against it.

    Attributes:
        data (pandas.DataFrame): Calgary Dog data
        breeds_list (list[str]) : list of breeds
        breeds_help (str) : stylized string of all breeds of dogs
        breed (str) : the name of the breed use for printing stats
    """
    data = pd.read_excel('Assets/CalgaryDogBreeds.xlsx', index_col=[0, 2])
    breeds_list : npt.NDArray[str] = data.index.unique(level=1).to_numpy()
    breeds_help: str = ',\n'.join([', '.join(x) for x in breeds_list.reshape(int(breeds_list.size / 10), 10)])
    idx = pd.IndexSlice

    def __init__(self, breed: str):
        self.breed = breed

    def print_top_years(self):
        """
        print years for the input breed where it has among top number of registrations
        """
        print(f'The {self.breed} was found in the top breeds for years: {
        ' '.join(str(x) for x in self.data.loc[self.idx[:, self.breed], :].index.unique(level=0))
        }')

    def print_total_registration(self):
        """
        print total registration for the input breed for all the data
        """
        print(f'There have been {
        self.data.loc[self.idx[:,self.breed], 'Total'].sum()
        } {self.breed} dogs registered total.')

    def print_yearly_perc_registration(self):
        """
        print yearly registration for the input breed as a percentage of overall registrations for that year
        """
        perc_yearly_total = (
                self.data.loc[self.idx[:, self.breed], 'Total'].groupby(level=0).sum() * 100 /
                self.data['Total'].groupby(level=0).sum()
        )

        [
            print(f'The {self.breed} was {v : .6f}% of the top breeds in {i}')
            for i, v in zip(perc_yearly_total.index, perc_yearly_total.values)
        ]

    def print_total_perc_registration(self):
        """
        print total registrations for the input breed as a percentage of overall registrations in the data
        """
        print(
            f'The {self.breed} was {
            self.data.loc[self.idx[:, self.breed], 'Total'].sum() * 100 / self.data['Total'].sum()
            : .6f}% of the top breed across all years.')

    def print_popular_months(self):
        """
        print months for input breed, where the input breed is top breed registered
        """
        months_sum = self.data.loc[self.idx[:, self.breed], :].groupby('Month', as_index=False).agg({'Total': 'sum'})
        months_sum_max = months_sum['Total'].max()
        log_10_power : int = int(math.log10(months_sum_max))
        log_10_multiplier: int = int(months_sum_max/ 10**log_10_power)
        max_threshold : int = log_10_multiplier * (10**log_10_power)

        print(
            f'Most popular month(s) for {self.breed} dogs: {
            ' '.join(months_sum[months_sum['Total'] > max_threshold]['Month'].unique())
            }')


def is_breed_not_in_data(input_breed : str) -> bool :
    """
    Helper method to check if a breed is not in the data.
    :param input_breed: breed of dog
    :type input_breed : str
    :return: true if breed is not in the data, false otherwise
    """
    return not np.any(CalgaryDogStore.breeds_list == input_breed)