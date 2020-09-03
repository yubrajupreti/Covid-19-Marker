from bottle import run, route, request, template, view, response
import csv


# opening csv file in read mode
with open('covid_countries.csv', 'r')as csv.file:
    csv_reader = csv.reader(csv.file)
    data = []

    # appending data from csv file to list.
    for read in csv_reader:
        data.append(read)


# route to this function with method post
@route('/getcountry',method='POST')

# @view is used to return template from map.html
@view('map')
def form_data():
    # the data from form is imported here
    country_name=request.forms.get('Country Name')

    # nested loop to find the data of country from the key word country_name
    for i in data:
        # import pdb;pdb.set_trace()
        for j in i:
            if country_name==j:

                # converting the data to dictionary type
                diced=dict(zip(data[0], i))

                # index() function to find index of the country enter in form
                data_index=data.index(i)

                # try...catch for the last index country. Hence last index country cause error here so it make run except block.
                #other country data for displaying as output from google map marker
                try:
                    country1=dict(zip(data[0],data[data_index+1]))
                    country2=dict(zip(data[0],data[data_index+2]))
                except:
                    country1 = dict(zip(data[0], data[data_index - 1]))
                    country2 = dict(zip(data[0], data[data_index - 2]))
                break



    return dict(dic=diced,c1=country1,c2=country2)


#For get request
@route('/getcountry')
def get_country():

    # making query
    country=request.query.country

    for i in data:
        # import pdb;pdb.set_trace()
        for j in i:
            if str(country)==j:
                dic=dict(zip(data[0],i))

    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Content-type'] = 'application/json'

    return dic

@route('/')
def form():
    return template('country_map')


if __name__=='__main__':
    run()






    # return open('covid_countries.csv',mode='r')
    # country=request.query.param1


    # return '<h1>The country is'+reader+'</h1>'

