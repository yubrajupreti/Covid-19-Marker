import petl as etl
import csv

# importing the data from csv file and converting the type of data.
table1=(etl.fromcsv('owid-covid-data.csv')
    .convert('iso_code','upper')
    .convert('location',str)
    .convert('date',str)
    .convert('total_cases', int)
    .convert('new_cases', int)
    .convert('total_deaths', int)
    .convert('new_deaths', int)
    .convert('total_cases_per_million', float)
    .convert('new_cases_per_million', float)
    .convert('total_deaths_per_million', float)
    .convert('new_deaths_per_million', float)
    .convert('total_tests', int)
    .convert('new_tests', int)
    .convert('total_tests_per_thousand', float)
    .convert('new_tests_per_thousand', float)
    .convert('tests_units', str)


)

# declaring a list of header that will be needed to make heading of the table
# other value will be appended from the for loop below
data1=[['iso_code','location','date','total_cases','new_cases','total_deaths','new_deaths','total_cases_per_million',
             'new_cases_per_million','total_deaths_per_million','new_deaths_per_million','total_tests','new_tests',
             'total_tests_per_thousand','new_tests_per_thousand','tests_units']]

# cut function is used to cut out the column given in the bracket below from the table
# cut function is not compulsory for table1 because the value given below are the total field that are present in table1
data=etl.cut(table1,'iso_code','location','date','total_cases','new_cases','total_deaths','new_deaths','total_cases_per_million',
             'new_cases_per_million','total_deaths_per_million','new_deaths_per_million','total_tests','new_tests',
             'total_tests_per_thousand','new_tests_per_thousand','tests_units')

# selecting the data from table on the basis of current date
# variable num consist of only the data of 2020-04-30 from each country.Hence the latest data is filter out.
num=etl.select(data,'date',lambda r:r=='2020-04-30')

# sort function is used to sort the unsorted data on the basis of iso_code
# thus ,this process help us to join the data easily in furthur steps
table1_sort=etl.sort(num,key='iso_code')

# counter variable is declared to count the number of country
count=0

# values function is used to read the data from table
for i in etl.values(table1_sort,'iso_code','location','date','total_cases','new_cases','total_deaths','new_deaths','total_cases_per_million',
             'new_cases_per_million','total_deaths_per_million','new_deaths_per_million','total_tests','new_tests',
             'total_tests_per_thousand','new_tests_per_thousand','tests_units'):

        # condition to take 15 countries from the table for intregration
        # thus 16 is given because when count will be 0 it contain the unnecessary data.
        if count==16:
            break

        # thus data1 was already declared with header on above code and other data are being appended
        data1.append(i)
        count=count+1

# removing the unnecessary data from the list which was in data1[1]
data1.pop(1)

# converting the list into tables
table_old=etl.head(data1,15)

# importing data from latest covid -19 data and converting the fields which will be needed
table2=(etl.fromcsv('current_covid.csv')
        .convert('median_age',float)
        .convert('aged_65_older',float)
        .convert('aged_70_older',float)

        )
# same as above table , list is declared with header
table2_header=[['iso_code','median_age','aged_65_older','aged_70_older']]
table2_data=etl.cut(table2,'iso_code','date','median_age','aged_65_older','aged_70_older')
table2_dated=etl.select(table2_data,'date',lambda v:v=='2020-04-30')
table2_sort=etl.sort(table2_dated,key='iso_code')

count=0
for j in etl.values(table2_sort,'iso_code','median_age','aged_65_older','aged_70_older'):
    if count == 15:
        break

    table2_header.append(j)
    count = count + 1

table_new=etl.head(table2_header,15)

# adding 3 column in table as per requirement
# join is used to join the table
final_table=etl.join(table_old,table_new,key='iso_code')
print(final_table)


# opening csv file in write mode and exporting data to csv file
with open('covid.csv','w') as f:
    writer=csv.writer(f)
    writer.writerows(final_table)
