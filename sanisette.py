import pandas as pd 
from back_end import Customer, i_need_to_pee


df = pd.read_csv('paris_sanisette.csv')
c1 = Customer(position=[48.862725, 2.287592], is_pmr=False, mode ='walk')
i_need_to_pee(c1, df)