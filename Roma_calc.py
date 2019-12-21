from math import factorial as fact

Error_list = [

    'Negative Value',

    'Wrong Value Syntax',

    'Result Too Long',

    'Error!',

]





class NegativeValue(Exception):

    pass



class WrongValue(Exception):

    pass



class WrongLength(Exception):

    pass



class NotBinary(Exception):

    pass







def value_check(num):

    if num < 0:

        raise NegativeValue



def numStr_check(numStr):

    if numStr.isdigit() == False:

        raise WrongValue



def length_check
