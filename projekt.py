"""
@mainpage Python Project

@section description_main Description
Projekt zaliczeniowy z przedmiotu Języki Skryptowe.
Program polega na stworzeniu modelu regresji liniowej zależności między PKB i konsumpcją. Stworzeniu jego podsumowania
na podstawie, którego zostały wyciągnięte wnioski i został on oceniony.
Stworzone również zostały dodatkowe wykresy: pudełkowe i wykresy zależności PKB od czasu dla każdego kraju.

Program pobiera dane o PKB i konsumpcji (źródło: https://data.oecd.org/gdp/gross-domestic-product-gdp.htm,
https://data.oecd.org/hha/household-spending.htm) z plików csv( consumption_data.csv, gdp_data.csv).
Są one wykorzystane do stworzenia modelu i wykresów za pomocą odpowiednich bibiliotek. Następnie w GUI użytkownik
może wyświetlić model regresji, jego podsumowanie i ocenę oraz wykresy pudełkowe, wykresy zależności PKB od czasu
dla konkretnego kraju, który użytkownik wybierze.

@section libraries_main Libraries/Modules
- pandas
- statsmodels.api
- matplotlib.pyplot
- matplotlib.backends.backend_tkagg
- tkinter

@section author_doxygen_example Author
- Justyna Sarkowicz gr 1
  Informatyka i Ekonometria
  I rok, stacjonarnie
"""

import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import *

# Importing data from OECD
consumption_data = pd.read_csv('consumption_data.csv')
gdp_data = pd.read_csv('gdp_data.csv')

# Data preprocessing
consumption_data = consumption_data[['LOCATION', 'Value']]
gdp_data = gdp_data[['LOCATION', 'Value']]
## Merging columns by LOCATION
data = pd.merge(consumption_data, gdp_data, on='LOCATION', suffixes=('_consumption', '_gdp'))
data = data.dropna()  # removing missing values
data = data.set_index('LOCATION')  # setting index
data = (data - data.min()) / (data.max() - data.min())  # min-max normalization
data = data.groupby(lambda x: x[:3], axis=0).sum()  # grouping data by region

# Model fitting and evaluation
X = data[['Value_consumption']]
y = data['Value_gdp']
X = sm.add_constant(X)
## Using OLS estimator
model = sm.OLS(y, X).fit()
## Summary of regression model
summary = model.summary()

## GUI setup
root = Tk()
root.title("Consumption and GDP in EU countries")
root.geometry("1000x750")


def regression_model():
    """ Creates a linear regression model, by using matplotlib.pyplot
        and display it on GUI. The data are normalized and grouped.
    """
    fig = plt.Figure(figsize=(7, 4), dpi=80)  # defining the chart size
    ax = fig.add_subplot(111)  # return an object in the grid
    ax.scatter(X['Value_consumption'], y)  # a scatter plot
    ax.plot(X['Value_consumption'], model.predict(X), color='pink')  # creating regression model
    ax.set_xlabel('Consumption')
    ax.set_ylabel('GDP')
    ax.set_title('Linear regression model of GPP and consumption in UE countries')
    # creating a canvas object
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().place(x=220, y=10)


def boxplots():
    """Creates a boxplots of consumption and GDP."""
    fig = plt.Figure(figsize=(7, 4), dpi=80)
    ax = fig.add_subplot(111)
    ax.boxplot([data['Value_consumption'], data['Value_gdp']])
    ax.set_xticklabels(['Consumption', 'GDP'])
    ax.set_ylabel('Dollars')
    ax.set_title('Boxplots of consumption and GDP in UE')
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().place(x=220, y=10)


def gdp_time(country_code):
    """ Create charts of GDP over time for country that user chose.
        @param country_code The selected value of the country code list.
        @return GDP plot over the time for selected country.
        If country is not selected it returns nothing.
    """
    if country_code == 'Select a country':
        return
    data_t = pd.read_csv('gdp_data.csv')
    country_data = data_t[data_t['LOCATION'] == country_code]  # comparing parametr with LOCATION
    dates = country_data['TIME'].tolist()
    gdp_values = country_data['Value'].tolist()
    fig = plt.Figure(figsize=(7, 4), dpi=80)
    ax = fig.add_subplot(111)
    ax.plot(dates, gdp_values)
    ax.set_xlabel('Time')
    ax.set_ylabel('GDP')
    ax.set_title('GDP in ' + country_code)
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().place(x=220, y=10)


def model_evaluation():
    """Display an interpretation of regression model on GUI."""
    interpretation = "By normalizing the data using Min-Max scaling, the range of the data is transformed" \
                     "to a fixed range between 0 and 1. This ensures that no variable dominates the model" \
                     "simply because it has larger values than others. This normalization allows for a fair" \
                     "comparison between the two variables, Consumption and GDP. The results show that the" \
                     "model has an R-squared value of 0.993, which means that 99.3% of the variation in GDP" \
                     "can be explained by the variation in consumption. The coefficient of the Value_consumption" \
                     " variable is 0.9208, which means that for every unit increase in consumption, there is" \
                     " an expected increase of 0.9208 units in GDP. Additionally, the p-value of the" \
                     "coefficient of the consumption variable is less than 0.05, indicating that it is " \
                     "statistically significant. Therefore, we can conclude that there is a significant" \
                     "positive relationship between consumption" \
                     "and GDP for EU countries. As consumption increases, GDP is expected to increase as well." \
                     "However, it is important to note that correlation does not imply causation and there may" \
                     "be other factors that are contributing to the relationship observed in the data."
    M.config(text=interpretation, justify='center', font='Helvetica 12')
    L.config(text='Evaluation of regression model', font='bold')


def model_summary():
    """Display the summary of regression model"""
    M.config(text=summary, font='Helvetica 8')
    L.config(text='Regression model summary')


## Configuration of text
M = Message(root, padx=10, pady=10, justify='center', font='Helvetica 8')
## Configuration of label
L = Label(root, font='bold')
M.place(x=220, y=370)
L.place(x=220, y=340)

selected_country = StringVar()
country_list = list(data.index.values.tolist())
selected_country.set('Select a country')
## Create a drop-down menu to select the country
country_menu = OptionMenu(root, selected_country, *country_list)
country_menu.config(width=18)

# Buttons
btn_gdp_over_time = Button(root, text="GDP over time", width=20, command=lambda: gdp_time(selected_country.get()))
btn_regression_model = Button(root, text="Regression model", width=20, command=regression_model)
btn_boxplots = Button(root, text="Boxplots", width=20, command=boxplots)
btn_model_evaluation = Button(root, text="Model evaluation ", width=20, command=model_evaluation)
btn_model_summary = Button(root, text="Model summary", width=20, command=model_summary)

# Add buttons to GUI window
btn_regression_model.place(x=10, y=10)
btn_boxplots.place(x=10, y=40)
country_menu.place(x=10, y=160)
btn_gdp_over_time.place(x=10, y=130)
btn_model_evaluation.place(x=10, y=70)
btn_model_summary.place(x=10, y=100)

## Run the GUI
root.mainloop()
