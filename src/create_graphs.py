import pandas as pd
import numpy as np
import altair as alt
pd.options.display.max_rows = 1000
pd.options.display.max_columns = 100

class GraphCreator:
    def __init__(self):
        self.__load_data()
        self.__clean_data()

    def general_stats(self):
        print(f'There are {self.data.shape[0]} responses after cleaning the data.')
        print(f'The average Base Salary is ${round(self.data["Base Salary"].mean(), 2)}.')
        print(f'The average Stock Option/Bonuses is ${round(self.data["Stock options and bonuses"].mean(), 2)}.')
        print(f'The average Total Pay is ${round(self.data["Total Pay"].mean(), 2)}.')

    def create_graphs(self):
        self.graph_pay_by("Role")
        self.graph_pay_by("Official Title")
        self.graph_pay_by("Level")
        self.graph_pay_by("General Title")
        self.graph_pay_by("Years in Tech")
        self.graph_pay_by("Job Count")
        self.graph_pay_by("Age")
        self.graph_pay_by("Education Level")
        self.graph_pay_by("Gender")
        self.graph_pay_by("Programming Language")
        self.graph_pay_by("Cloud based")
        self.graph_pay_by("Remote")
        self.graph_pay_by("Metropolian Area")

    def graph_pay_by(self, x_axis):
        base_pay = self.data.groupby(x_axis, as_index=False)['Base Salary'].mean()
        base_pay = base_pay.rename(columns={"Base Salary": "pay"})
        base_pay['pay type'] = "Salary"

        bonus_pay = self.data.groupby(x_axis, as_index=False)['Stock options and bonuses'].mean()
        bonus_pay = bonus_pay.rename(columns={"Stock options and bonuses": "pay"})
        bonus_pay['pay type'] = "Bonuses and Stock Options"
        both_pay = bonus_pay.append(base_pay, ignore_index=True)

        chart = alt.Chart(both_pay).mark_bar().encode(
            x = alt.X(x_axis,
                sort=alt.EncodingSortField(field = 'pay', op = "sum")),
            y = 'sum(pay)',
            color = alt.Color("pay type", sort="descending")
        ).properties(
            title=f'Average Base Salary by {x_axis}'
        )
        chart.save(f'../graphs/2019/Pay By {x_axis}.png')

    def __load_data(self):
        self.file_location = "../salary-results-2019.csv"
        self.data = pd.read_csv(self.file_location, header=0, index_col=False, names=self.__columns())

    def __clean_data(self):
        self.data = self.data.reset_index()
        self.data['Stock options and bonuses'] = self.data['Stock options and bonuses'].fillna(0)
        self.data = self.data[self.data['Base Salary'] > 1000]
        self.data['Total Pay'] = self.data['Base Salary'] + self.data['Stock options and bonuses']

    def __columns(self):
        return [
            "Role",
            "Official Title",
            "Level",
            "General Title",
            "Years in Tech",
            "Job Count",
            "Age",
            "Education Level",
            "Gender",
            "Base Salary",
            "Programming Language",
            "Cloud based",
            "Remote",
            "Metropolian Area",
            "Stock options and bonuses",
        ]

creator = GraphCreator()
creator.general_stats()
creator.create_graphs()
