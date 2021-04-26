import numpy as np

# used to stored the data of each instance user in the users.csv file
class Person:
    def __init__(self, account_id=np.NaN, first_name=np.NaN, last_name=np.NaN, password=np.NaN, balance=0):
        self.account_id = account_id
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.balance = balance

