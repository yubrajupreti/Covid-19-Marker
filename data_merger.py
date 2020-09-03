import petl as etl
import csv

table1=(etl.fromcsv('covid.csv'))

# importing data from xml file and creating table
table2 = etl.fromxml('Country_location.xml','.//tr',('th','td'))
# print(table2)

# removing column country from table
table3=etl.cutout(table2,'country')

# merging the covid table with xml data
table4=etl.join(table1,table3,key='location')
print(table4)

# writing result to csv file
with open('covid_countries.csv','w') as f:
    writer=csv.writer(f)
    writer.writerows(table4)