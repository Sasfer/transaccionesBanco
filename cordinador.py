import threading
import time
import socket
import os
import threading
import signal
from datetime import timedelta 
"""TODO:
TIMEOUT DE 2 SEGUNDOS
msg de timeout

"""

#Global Variables 
balance = 100.0
current_token = None
expiration = None
is_locked = False
lock = threading.Lock()

#Utilieties 
def gen_password(length=8, charset="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789()"):
    random_bytes = os.urandom(length)
    len_charset = len(charset)
    indices = [int(len_charset * (ord(byte) / 256.0)) for byte in random_bytes]
    return "".join([charset[index] for index in indices])


class Transaction():
    def __init__(self,balance):
        self.balance = balance

    def get_balance(self):
        return self.balance
        
    def increase(self, porcentage):
        self.balance = (self.balance) * (1+(porcentage/100.0))
        return self.balance

    def deposit(self, amount):
        self.balance += amount 
        return self.balance

    def withdraw(self, amount):
        self.balance -= amount 
        return self.balance

class Coordinator():
    def __init__(self):
        global balance
        self.balance = balance # global

    def timeout(self):
        global expiration
        expiration = time.time()
        expiration += 2.0
        print('TODO: TIMEOUT ')


    def open_trans(self):
        global is_locked,current_token
        print('islocked',is_locked)
        self.timeout() # INIT TIMEOUT
        if(is_locked):
            return self.abort_trans('Resource is being used by other User')
        else:
            current_token = gen_password()
            #is_locked = True
            return self.token(current_token)
        
    def do(self, token, move, params=None):
        global is_locked,current_token
        if(token != current_token and is_locked == False and move == 'get_balance'):
            t = Transaction(self.balance)
            return t.get_balance()

        if(token != current_token):
            print(':: TIMEOUT EXPIRED SERVER ::' )
            return self.abort_trans('Token Expired!')
        
        if(expiration < time.time() ):
            print(':: TOKEN EXPIRED SERVER ::' , token )
            return self.abort_trans('Timeout, session expired')

        if(move == 'get_balance'):
            print('coord::balance')
            t = Transaction(self.balance)
            return t.get_balance()

        elif(move == 'increase'):
            print('coord::increase')
            is_locked = True
            t = Transaction(self.balance)
            self.balance = t.increase(params)
            return self.balance

        elif(move == 'deposit'):
            is_locked = True
            print('coord::deposit')
            is_locked = True
            t = Transaction(self.balance)
            self.balance = t.deposit(params)
            return self.balance

        elif(move == 'withdraw'):
            is_locked = True
            print('coord::withdraw')
            t = Transaction(self.balance)
            is_locked = True
            self.balance = t.withdraw(params)
            return self.balance

        elif(move == 'close_session'):
            print('coord::close_session')
            t = Transaction(self.balance)
            new_balance = t.get_balance()
            if(new_balance >= 0):
                return self.close_trans(new_balance)
            else:
                return self.abort_trans('Not Enough Money!')


    def close_trans(self,new_balance):
        global is_locked,current_token
        print('coord::close_session')
        balance = new_balance
        self.balance = balance
        is_locked = False
        current_token = None
        #print('balance',balance)
        return balance
    
    def token(self,token):
        print('curr', token)
        return token

    def abort_trans(self,message):
        global is_locked,current_token
        print('coord::abort_trans')
        is_locked = False
        current_token = None
        self.balance = balance # RESET BALANCE
        return message