import seaborn as sns
import matplotlib.pyplot as plt
import math 
import random
import datetime
import sys
import json

begin_time = datetime.datetime.now()
simulation_time = int
global_sentiment = random.choice(["bullish", "bearish"])
global_market = False
global_market_strength = 5 #smaller global_market_strength is stronger effect
average_change_global_sentiment = float #1 / (days * 24 * number_of_stocks) changes every * days
simulation_time = 1
save = False
save_fig = False
save_mode = 0 #0: save all data points, 1: save only last data point

def get_input():
    global simulation_time
    global global_market
    global global_market_strength
    global save
    global save_fig
    global simulation_time
    global save_mode
    global average_change_global_sentiment
    
    stock_list = []
    
    #simple-stock_market.py json.txt simulation_time(int) save(0,1) save_fig(0,1), save_mode(0,1) global_market(0,1) global_market_strength(int)
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
            simulation_time = abs(int(sys.argv[2]))
            save_input = int(sys.argv[3])
            if save_input == 1:
                save = True
            save_fig_input = int(sys.argv[4])
            if save_fig_input == 1:
                save_fig = True
            save_mode_input = int(sys.argv[5])
            if save_mode_input == 1:
                save_mode = 1
            global_market_input = abs(int(sys.argv[6]))
            if global_market_input == 1:
                global_market = True
            global_market_strength = abs(int(sys.argv[7]))
                
        except:
            pass
        
    else:
        try:
            number_of_stocks = abs(int(input("Enter a number of stocks: ")))
            simulation_time = abs(int(input("Enter a simulation time (days) (int): "))) #days
            global_market = input("Global market (y/n): ") #days
            if global_market == "y":
                global_market = True
                global_market_strength = abs(int(input("Enter global market strenght (lower is stronger) (default: 5) (int): ")))
                if global_market_strength == 0:
                    global_market_strength = 1
            else:
                global_market = False
            save_input = input("Create output (y/n): ") #days
            if save_input == "y":
                save = True
            save_fig_input = input("Save figure (y/n): ") #days
            if save_fig_input == "y":
                save_fig = True
            save_mode_input = input("Store only last value (0,1): ") #days
            if save_mode_input == "1":
                save_mode = 1
            
    
        except:
            print("please enter a number")
            exit()    
    
        for z in range(number_of_stocks): 
            try:
                last_change = random.choice(["positive", "negative"])
                min_price = abs(float(input("Enter a min stock price: ")))
                if min_price == 0:
                    min_price = 1
                max_price = abs(float(input("Enter a max stock price: ")))
                if max_price == 0:
                    max_price = 1
                current_price = abs(float(input("Enter a current stock price: ")))
                if current_price == 0:
                    current_price = 1
                volatility = abs(float(input("Enter a stock volatility (0.1-0.9): "))) #determines width of min max range
                if volatility == 0:
                    volatility = 0.1
                value_scaler = abs(float(input("Enter a stock value scaler: "))) #determines cheapness of stock
                if value_scaler == 0:
                    value_scaler = 1
                stock_name = input("Enter a stock name: ") #determines cheapness of stock
                
                stock_dict = {
                    "time": [],
                    "current_price": []
                }
                
                stockdict =	{
                    "last_change": last_change,
                    "min_price": min_price,
                    "max_price": max_price,
                    "current_price": current_price,
                    "volatility": volatility,
                    "value_scaler": value_scaler,
                    "stock_dict": stock_dict,
                    "stock_name": stock_name
                }
                
                stock_list.append(stockdict)
            
            except:
                print("please enter a number")
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
        stock_dict = stock.get("stock_dict")
        stock_name = stock.get("stock_name")
        
        plot = sns.lineplot(x=stock_dict['time'], y=stock_dict['current_price']).get_figure()
        plot.savefig(stock_name+".png", format='png', dpi=1250)
        plt.close() 

def check_save(stock_dict):
    global simulation_time
    time_list = stock_dict['stock_dict']['time']
    if not time_list:
        return 0
    else:
        start_time = int(round(len(time_list) / 60 / 24))
        simulation_time = simulation_time + start_time
        return start_time
    
def save_json(stock_list):
    f = open("output.txt", "w+")
    f.close()
    
    for stock_dict in stock_list:
        json_object = json.dumps(stock_dict) 
        
        f = open("output.txt", "a")
        f.write(json_object)
        f.write("\n")
        f.close()

def run():
    global save
    global save_fig
    global simulation_time
    global save_mode
    
    stock_list = get_input()
    
    start_time = check_save(stock_list[0])
    
    for q in range(start_time, simulation_time):
        print("time: " + str(q))
        for stock_index, stock in enumerate(stock_list):  
              
            min_price = stock.get('min_price')
            max_price = stock.get('max_price')
            current_price = stock.get('current_price')
            volatility = stock.get('volatility')
            value_scaler = stock.get('value_scaler')
            last_change = stock.get('last_change')
            stock_dict = stock.get("stock_dict")
        
            function = define_function(current_price, max_price, min_price)
            time = q * 60 * 24
            
            for i in range(24):
                price_target = get_price_target(function, i, max_price, min_price,)
                
                for j in range(60):
                    update_current_price_result = (update_current_price(current_price, max_price, min_price, price_target, last_change))
                    current_price = update_current_price_result[0]
                    
                    scaled_current_price = scale_value(current_price, value_scaler)
                    last_change = update_current_price_result[1]
                    
                    time_list = stock_dict['time']
                    current_price_list = stock_dict['current_price']
                    
                    if save_mode == 1:
                        time_list = []
                        current_price_list = []

                    time_list.append(time)
                    current_price_list.append(scaled_current_price)

                    stock_dict['time'] = time_list
                    stock_dict['current_price'] = current_price_list
                    
                    time = time + 1
                    
                new_min_max_prize = update_min_max(max_price, min_price, volatility)
                max_price = new_min_max_prize[0]
                min_price = new_min_max_prize[1]
                
            stock['min_price'] = min_price
            stock['max_price'] = max_price
            stock['current_price'] = current_price
            stock['last_change'] = last_change
            stock['stock_dict'] = stock_dict
            
            stock_list[stock_index] = stock
    
    if save_fig == True:
        plot_stock_value(stock_list)    

    if save == True:
        save_json(stock_list)  
         
    print("Runtime: " + str(datetime.datetime.now() - begin_time))
    
run()