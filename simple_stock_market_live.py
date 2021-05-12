import seaborn as sns
import matplotlib.pyplot as plt
import math 
import random
import sys
import json
import threading

global_sentiment = random.choice(["bullish", "bearish"])
global_market = False
global_market_strength = 4 #smaller global_market_strength is stronger effect
average_change_global_sentiment = float #1 / (days * 24 * number_of_stocks) changes every * days
save = False
save_fig = False
save_mode = 0 #0: save all data points, 1: save only last data point

hour = 0
minute = 0

def get_input():
    global global_market
    global global_market_strength
    global save
    global save_fig
    global save_mode
    global average_change_global_sentiment
    
    stock_list = []
    
    #simple-stock_market.py json.txt save(0,1) save_fig(0,1), save_mode(0,1) global_market(0,1) global_market_strength(float)
    if len(sys.argv) > 1:
        input_json_file = sys.argv[1]
        
        try:
            with open(input_json_file) as f:
                for jsonObj in f:
                    stockdict = json.loads(jsonObj)
                    stock_list.append(stockdict)
        except:
            print("Error in file")
            exit()  
            
        try:
            save_input = int(sys.argv[2])
            if save_input == 1:
                save = True
            save_fig_input = int(sys.argv[3])
            if save_fig_input == 1:
                save_fig = True
            save_mode_input = int(sys.argv[4])
            if save_mode_input == 1:
                save_mode = 1
            global_market_input = abs(int(sys.argv[5]))
            if global_market_input == 1:
                global_market = True
            global_market_strength = abs(float(sys.argv[6]))
                
        except:
            pass
    else:
        print("please provide an input file")
        exit()
            
    average_change_global_sentiment = 1 / (100 * 24 * len(stock_list))
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

def get_price_target(function, time_step, max_price, min_price):
    global global_market
    global global_sentiment
    global global_market_strength
    global average_change_global_sentiment

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
        
    if global_market == True:
        rand_global_sentiment_value = random.random()
        if rand_global_sentiment_value < average_change_global_sentiment:
            global_sentiment = random.choice(["bullish", "bearish"])
                
        if global_sentiment == "bullish":
            rand_global_market_value = random.random() / (global_market_strength / price_target)
            price_target = price_target + rand_global_market_value
        elif global_sentiment == "bearish":
            rand_global_market_value = -1 * random.random() / (global_market_strength / price_target)
            if price_target + rand_global_market_value > 0:
                price_target = price_target + rand_global_market_value
                
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
        if new_price - rand_pos_value < 0.001:
            rand_pos_change_2 = random.random() / 100
            while new_price - ( rand_pos_change - rand_pos_change_2 ) < 0.001:
                rand_pos_change_2 = random.random()
            new_price = new_price - ( rand_pos_change - rand_pos_change_2 )
        else:
            new_price = new_price - rand_pos_value
    elif last_change == "positive":
        new_price = new_price + rand_pos_value

    return [new_price, last_change]

def update_min_max(max_price, min_price, volatility):    
    prefered_diff = -3.300066 + 3.44987 * math.pow(math.e, 3.660217 * volatility)
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
        stock_dict = stock.get("stock_dict")
        stock_name = stock.get("stock_name")
        
        plot = sns.lineplot(x=stock_dict['time'], y=stock_dict['current_price']).get_figure()
        plot.savefig(stock_name+".png", format='png', dpi=1250)
        plt.close() 

def check_save(stock_dict):
    time_list = stock_dict['stock_dict']['time']
    if not time_list:
        return 0
    else:
        start_time = int(round(len(time_list) / 60 / 24))
        return start_time
    
def save_json():
    global stock_list
    
    f = open("output.txt", "w+")
    f.close()
    
    for stock_dict in stock_list:
        save_dict = stock_dict.copy()
        del save_dict['function']
        del save_dict['price_target']
        
        json_object = json.dumps(save_dict) 
        
        f = open("output.txt", "a")
        f.write(json_object)
        f.write("\n")
        f.close()

def days():
    global stock_list
    global hour
    
    for stock_index, stock in enumerate(stock_list):  
        min_price = stock.get('min_price')
        max_price = stock.get('max_price')
        current_price = stock.get('current_price')
        volatility = stock.get('volatility')
        value_scaler = stock.get('value_scaler')
        last_change = stock.get('last_change')
        stock_dict = stock.get("stock_dict")
    
        function = define_function(current_price, max_price, min_price)
        stock['function'] = function
        stock_list[stock_index] = stock
        
    hour = 0
    
    threading.Timer(86400.0, days).start()
        
def hours():
    global stock_list
    global hour
    global minute
    
    for stock_index, stock in enumerate(stock_list):  
        min_price = stock.get('min_price')
        max_price = stock.get('max_price')
        current_price = stock.get('current_price')
        volatility = stock.get('volatility')
        value_scaler = stock.get('value_scaler')
        last_change = stock.get('last_change')
        stock_dict = stock.get("stock_dict")   
        function = stock.get("function")   
        
        price_target = get_price_target(function, hour, max_price, min_price,)
        
        new_min_max_prize = update_min_max(max_price, min_price, volatility)
        max_price = new_min_max_prize[0]
        min_price = new_min_max_prize[1]
        
        stock['price_target'] = price_target
        stock['max_price'] = max_price
        stock['min_price'] = min_price
        stock_list[stock_index] = stock
        
    hour = hour + 1
    minute = 0
        
    threading.Timer(3600.0, hours).start()
  
def minutes():
    global save
    global save_fig
    global save_mode
    global stock_list
    global minute
    
    for stock_index, stock in enumerate(stock_list):  
        min_price = stock.get('min_price')
        max_price = stock.get('max_price')
        current_price = stock.get('current_price')
        volatility = stock.get('volatility')
        value_scaler = stock.get('value_scaler')
        last_change = stock.get('last_change')
        stock_dict = stock.get("stock_dict")   
        function = stock.get("function") 
        price_target = stock.get("price_target") 
        update_current_price_result = (update_current_price(current_price, max_price, min_price, price_target, last_change))
        current_price = update_current_price_result[0]
        
        scaled_current_price = scale_value(current_price, value_scaler)
        last_change = update_current_price_result[1]
        
        time_list = stock_dict['time']
        try:
            time = time_list[-1]
            time = time + 1
        except:
            time = 0
            
        current_price_list = stock_dict['current_price']
        
        if save_mode == 1:
            time_list = []
            current_price_list = []

        time_list.append(time)
        current_price_list.append(scaled_current_price)

        stock_dict['time'] = time_list
        stock_dict['current_price'] = current_price_list
        
        stock['current_price'] = current_price
        stock['last_change'] = last_change
        stock['stock_dict'] = stock_dict
        
        stock_list[stock_index] = stock
        
        print(scaled_current_price)
        
    if save_fig == True:
        plot_stock_value(stock_list)    

    if save == True:
        save_json()  
          
    minute = minute + 1
        
    threading.Timer(60.0, minutes).start()
  

def run():
    global stock_list
    
    stock_list = get_input()
    days()
    hours()
    minutes()

                 
run()