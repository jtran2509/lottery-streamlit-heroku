import streamlit as st

import numpy as np
import pandas as pd

st.title('Your chances of winning is...')

st.header('About this calculator')

st.markdown('**Fictional scenario:** To prevent and treat gambling addictions, a medical institute wants to build a dedicated mobile app to help lottery addicts better estimate their chances of winning')

st.markdown("We'll consider historical dataset coming from the national 6/49 lottery game in Canada with 3665 drawings, dating from 1982 to 2018")


from PIL import Image 

ig = Image.open('lottery.jpg')
st.image(ig, caption = '6/49 Lottery')

def factorial(n):
    """Computes the factorial of the number n
    
    Args:
        n(int): the number to compute for
        
    Returns:
        n(int): the results
    """
    final_product = 1
    for i in range(n, 0, -1):
        final_product *= i
    return final_product

def combinations (n,k):
    """Computes the number of combinations when taking only k objects
from a group of n objects

    Args:
        k (int): number of groups
        n (int): the number of objects
    Returns:
        n(int): results
    """
    numerator = factorial(n)
    denominator = factorial(k) * (factorial(n-k))
    return numerator/denominator

def one_ticket_probability(k, n):
    """Takes in a list of 6 numbers and prints the probability of winning
in a way that's easy to understand

    Args:
        k (int): The number of objects wants to sample
        n (int): Total possible number
    
    Returns:
        n (float): probability of winning

"""
    possible_outcomes = combinations(n, k)
    successful_outcome = 1 # We assume that the player only buy 1 ticket
    prob_1_ticket = successful_outcome / possible_outcomes
    percentage = prob_1_ticket
    
    return ('Your probability of winning is: {:.8f}'.format(percentage))

st.header('Less winning numbers')
st.markdown('Suppose you only have **1 ticket**, here is your probability of 2,3,4, or 5 winning numbers')


def probability_less_6(input_num):
    combination = combinations(6, input_num)
    success_outcome = combinations(43, 6 - input_num)
    total_success_outcome = combination * success_outcome
    winning_prob = total_success_outcome /combinations(49,6)
    winning_perct = winning_prob * 100
    
    return ('The probability of {} winning numbers is: {:.4f}%'.format(input_num, winning_perct))
    

th = st.number_input('Please enter a value between 2 and 6', min_value = 2, max_value = 5, step = 1)    
st.write(probability_less_6(int(th)))

st.header('Multi-ticket probability winning:')
st.markdown('If you have more than 1 ticket, here is your probability of winning:')

def multi_ticket_probability(ticket_num):
    possible_outcomes = combinations(49,6)
    successful_outcome = int(ticket_num)
    win_prob = successful_outcome / possible_outcomes
    win_perc = win_prob * 100
    return win_perc

x = st.slider('Choose between 1 & 100', min_value = 1,
              max_value = 100, step = 1)

st.write('Your probability of winning the big prize is: {:.10f}'.format(multi_ticket_probability(ticket_num = x)) )

    
    
from pathlib import Path 
st.header('Historical Data Check')
lottery = pd.read_csv('649.csv')



st.markdown("Based on the numbers you provide, we'll use the historical data as described above to determine whether you would have ever won by now!")

def extract_numbers(row):
    row = row[4:10]
    row = set(row.values)
    return row

## Apply to a whole dataframe
winning_num = lottery.apply(extract_numbers, axis = 1)

def check_historical_occurence(user_num, win_num):
    user_num = set(user_num)
    occurence_check = user_num == win_num
    num_occur = occurence_check.sum()
    if num_occur == 1:
        return("Congratulations! This set of numbers has occurred {} times".format(num_occur)) + ". " + one_ticket_probability(6, 49)
    else:
        return ("Sorry! You can save your money for something else!")
        
import re
collect_number = lambda x :[int(i) for i in re.split('[^0-9]', x) if i != '']
numbers = st.text_input('''Please enter your ticket numbers!
                           E.g. Try this: 1, 6, 39, 23, 24, 27
''')
numbers = collect_number(numbers)
st.write(check_historical_occurence(numbers, winning_num))
