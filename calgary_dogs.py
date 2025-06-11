# calgary_dogs.py
# Danish Shahid
#
# A terminal-based application for computing and printing statistics based on given input.
# Detailed specifications are provided via the Assignment 4 README file.
# You must include the main listed below. You may add your own additional classes, functions, variables, etc. 
# You may import any modules from the standard Python library.
# Remember to include docstrings and comments.

from CalgaryDogsStore import *

def main():
    print("ENSF 692 Dogs of Calgary")

    # User input stage
    is_breed_not_found : bool = True
    retry : int = 0
    dog_breed_input: str = ""
    while is_breed_not_found:
        try :
            # setting up prompt string - include dog names if first attempt else don't
            input_prompt : str = f"Enter a dog breed from the following options{f'\n{CalgaryDogStore.breeds_help}' if retry == 0 else ''}: "

            # make the input upper to compare with the dataset
            dog_breed_input =  input(input_prompt).upper()

            # set retry to not include unique dog list on second attemp
            retry += 1

            # check whether breed found in data
            is_breed_not_found = is_breed_not_in_data(dog_breed_input)

            # raise error if not found
            if is_breed_not_found:
                raise KeyError('Dog breed not found in the data. Please try again.')

        except KeyError as e:
            print(e.args[0])

    # create an object
    cds: CalgaryDogStore = CalgaryDogStore(dog_breed_input)

    # Data analysis stage
    #top breed in the year
    cds.print_top_years()

    #total breeds registered
    cds.print_total_registration()

    #breed percentage for each year
    cds.print_yearly_perc_registration()

    #breed percentage for all years
    cds.print_total_perc_registration()

    #months when input is the top dog
    cds.print_popular_months()

if __name__ == '__main__':
    main()
