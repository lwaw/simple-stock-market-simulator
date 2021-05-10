import seaborn as sns
import matplotlib.pyplot as plt
import math 
import random
import datetime
import pandas as pd

begin_time = datetime.datetime.now()
#remove_nth_row = int
simulation_time = int

def get_input():
    global simulation_time
    #global remove_nth_row
    
    try:
        number_of_stocks = abs(int(input("Enter a number of stocks: ")))
        simulation_time = abs(int(input("Enter a simulation time (days) (int): "))) #days
        #plot_npercent_of_data = abs(int(input("How many percent of the data should be plotted: "))) #keep file size small
        
        #if plot_npercent_of_data != 100:
        #    remove_nth_row = int((simulation_time * 24 * 60 * 0.01) / (simulation_time * 24 * 60 * 0.01 * (100 - plot_npercent_of_data)))
        #else:
        #    remove_nth_row = 0
    except:
        print("please enter a number")
        exit()    
    
    stock_list = []
    for z in range(number_of_stocks): 
        try:
            last_change = random.choice(["positive", "negative"])
            min_price = abs(float(input("Enter a min stock price: ")))
            max_price = abs(float(input("Enter a max stock price: ")))
            current_price = abs(float(input("Enter a current stock price: ")))
            volatility = abs(float(input("Enter a stock volatility (0.1-0.9): "))) #determines width of min max range
            value_scaler = abs(float(input("Enter a stock value scaler: "))) #determines cheapness of stock
            stock_name = input("Enter a stock name: ") #determines cheapness of stock
                
            stock_df = pd.DataFrame(columns=['time','current_price'])
            
            stockdict =	{
                "last_change": last_change,
                "min_price": min_price,
                "max_price": max_price,
                "current_price": current_price,
                "volatility": volatility,
                "value_scaler": value_scaler,
                "stock_df": stock_df,
                "stock_name": stock_name
            }
            
            stock_list.append(stockdict)
            
        except:
            print("please enter a number")
            exit()   
            
    return(stock_list)

def define_function(current_price, max_price, min_price):
    use_current_price = current_price
    function_type = random.choice(["sin", "cos"])

    number_of_periods = int(round((1 + random.random())))
    period_length = 24 / number_of_periods
    periodicity = (2 * math.pi) / period_length

    amplitude = ((max_price - min_price) / 100) * random.random()
    
    if function_type == "sin":
        vertical_translation = use_current_price
    elif function_type == "cos":
        vertical_translation = use_current_price

    function = {
        "periodicity": periodicity,
        "amplitude": amplitude,
        "vertical_translation": vertical_translation,
        "function_type": function_type
    }

    return function

def get_price_target(function, time_step, max_price, min_price,):
    if function.get('function_type') == "sin":
        price_target = function.get('amplitude') * math.sin(function.get('periodicity') * time_step) + function.get('vertical_translation')
    elif function.get('function_type') == "cos":
        price_target = function.get('amplitude') * math.cos(function.get('periodicity') * time_step) + function.get('vertical_translation')
    
    rand_pos_change = random.random()
    rand_pos_change_pos_neg = random.random()
    if rand_pos_change < 1:
        if rand_pos_change_pos_neg < 0.5:
            price_target = price_target - ((max_price - min_price) * (random.uniform(0.1, 1.0) / 10) )
        elif rand_pos_change_pos_neg > 0.5:
            price_target = price_target + ((max_price - min_price) * (random.uniform(0.1, 1.0) / 10) )
    
    if price_target < min_price:
        price_target = min_price
    elif price_target > max_price:
        price_target = max_price
        
    return price_target

def update_current_price(current_price, max_price, min_price, price_target, last_change):  
    new_price = current_price + (price_target - current_price) * random.random() / 100
    rand_pos_change = random.random()
    rand_pos_value = ((max_price - min_price) * (random.uniform(0.1, 1.0) / 10) ) / 100

    if rand_pos_change < 0.1:
        if last_change == "negative":
            last_change = "positive"
        else:
            last_change = "negative"
            
    if last_change == "negative":
        new_price = new_price - rand_pos_value
    elif last_change == "positive":
        new_price = new_price + rand_pos_value

    return [new_price, last_change]

def update_min_max(max_price, min_price, volatility):
    prefered_diff = math.pow(-3.300066 + 3.44987 * math.e, 3.660217 * volatility)
    diff = max_price - min_price
    rand_change_max_value = random.random()
    rand_change_min_value = random.random()
    
    if rand_change_max_value < 0.1:
        if diff > prefered_diff:
            new_max_price = max_price - random.random()
        else:
            new_max_price = max_price + random.random()
    else:
        new_min_price = min_price
        new_max_price = max_price
        
    if rand_change_min_value < 0.1:
        if diff > prefered_diff:
            new_min_price = min_price + random.random()
        else:
            new_min_price = min_price - random.random()
    else:
        new_min_price = min_price
        new_max_price = max_price
        
    if new_min_price > new_max_price:
        new_min_price = min_price
        new_max_price = max_price
        
    if new_min_price <= 0:
        new_min_price = min_price
    if new_max_price <= 0:
        new_min_price = max_price
    
    return [new_max_price, new_min_price]

def scale_value(value, value_scaler):
    new_value = value / value_scaler
    return new_value

def plot_stock_value(stock_list):
    for stock_index, stock in enumerate(stock_list):
        stock_df = stock.get("stock_df")
        stock_name = stock.get("stock_name")
        
        #if remove_nth_row != 0:
        #stock_df = stock_df.iloc[::remove_nth_row, :]
        
        plot = sns.lineplot(data=stock_df, x="time", y="current_price").get_figure()
        plot.savefig(stock_name+".png", format='png', dpi=1250)
        plt.close() 

stock_list = get_input()

def run():
    for q in range(simulation_time):
        print("time: " + str(q))
        for stock_index, stock in enumerate(stock_list):  
              
            min_price = stock.get('min_price')
            max_price = stock.get('max_price')
            current_price = stock.get('current_price')
            volatility = stock.get('volatility')
            value_scaler = stock.get('value_scaler')
            last_change = stock.get('last_change')
            stock_df = stock.get("stock_df")
        
            function = define_function(current_price, max_price, min_price)
            time = q * 60 * 24
            
            for i in range(24):
                price_target = get_price_target(function, i, max_price, min_price,)
                
                for j in range(60):
                    update_current_price_result = (update_current_price(current_price, max_price, min_price, price_target, last_change))
                    current_price = update_current_price_result[0]
                    
                    scaled_current_price = scale_value(current_price, value_scaler)
                    last_change = update_current_price_result[1]
                    
                    new_row = {'time':time, 'current_price':scaled_current_price}
                    stock_df = stock_df.append(new_row, ignore_index=True)
                    
                    time = time + 1
                    
                new_min_max_prize = update_min_max(max_price, min_price, volatility)
                max_price = new_min_max_prize[0]
                min_price = new_min_max_prize[1]
                
            stock['min_price'] = min_price
            stock['max_price'] = max_price
            stock['current_price'] = current_price
            stock['stock_index'] = stock
            stock['last_change'] = last_change
            stock['stock_df'] = stock_df
            
            stock_list[stock_index] = stock
    
    plot_stock_value(stock_list)                  
    print("Runtime: " + str(datetime.datetime.now() - begin_time))
    
run()