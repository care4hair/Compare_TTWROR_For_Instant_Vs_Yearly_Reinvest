import numpy as np
import matplotlib.pyplot as plt


years = 10
days_per_year = 365
time_in_days = np.arange(0,years * days_per_year-1)

initial_invest = 100
assumed_growth_per_day = 0.03/days_per_year
assumed_dividend_percentage = 0.01
assumed_time_between_dividends_in_days = 100

# instant_reinvest: True - sofortiger Reinvest, False - Invest zum Jahresende)
def simulate_portfolio(instant_reinvest) :
    invested = np.zeros(time_in_days.size)
    invested[0] = initial_invest
    
    uninvested = 0
    reinvested = 0
    
    total = np.zeros(time_in_days.size)
    total[0] = invested[0] + uninvested
    ttwror = 1
    dividend = np.zeros(time_in_days.size)
    for day in time_in_days:
        if (day % assumed_time_between_dividends_in_days) == 0:
            dividend[day]=assumed_dividend_percentage

    for day in time_in_days[1:]:
        invest = 0
        uninvested = uninvested + dividend[day]*invested[day-1]
        if (instant_reinvest or (day % days_per_year == 0) or (day == time_in_days[-1])):
            invest = uninvested
            reinvested = reinvested + invest
            uninvested = 0
        
        invested[day] = invested[day-1] * (1 + assumed_growth_per_day) + invest
        total[day] = invested[day] + uninvested
        return_in_period = (total[day]-total[day-1])/total[day-1]
        ttwror = ttwror * (1 + return_in_period)
    ttwror = ttwror - 1
    return total, ttwror, reinvested
  
total_instant, ttwror_instant, reinvested_instant = simulate_portfolio(True)
total_yearly, ttwror_yearly, reinvested_yearly = simulate_portfolio(False)

print("TTWROR: true time weighted rate of return")
print(f" instant: {(ttwror_instant*100):.2f}%")
print(f" yearly:  {(ttwror_yearly*100):.2f}%")
print(f"Total instant: {(total_instant[-1]):.2f} EUR")
print(f"Total yearly: {(total_yearly[-1]):.2f} EUR")
print(f"Total dividends instant: {(reinvested_instant):.2f} EUR")
print(f"Total dividends yearly: {(reinvested_yearly):.2f} EUR")

fig, ax = plt.subplots()     
ax.plot(time_in_days, total_instant, label='instant reinvest')
ax.plot(time_in_days, total_yearly, label='yearly reinvest')
ax.set_xlabel('days')
ax.set_ylabel('portfolio total') 
ax.legend()
ax.set_title("Comparison of instant vs yearly reinvest of dividends")  
plt.show()    

