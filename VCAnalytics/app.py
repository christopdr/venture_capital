import os

import pandas as pd
import numpy as np
import pymongo
import json
from flask import Flask, jsonify, render_template


app = Flask(__name__)

client = pymongo.MongoClient("mongodb+srv://adminUsr:mongo1234@venturecapital-mmycs.mongodb.net/admin?retryWrites=true")
db = client.VentureCapital
collection = db.LATAMtb

app.config.update(
    JSON_AS_ASCII= True
)
##
#################################################
# Database Setup
#################################################

#app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/bellybutton.sqlite"
#db = SQLAlchemy(app)

# reflect an existing database into a new model
#Base = automap_base()
# reflect the tables
#Base.prepare(db.engine, reflect=True)

# Save references to each table
#Samples_Metadata = Base.classes.sample_metadata
#Samples = Base.classes.samples


@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")



########INDEX LINKS######################

@app.route("/dynamicData")
def dynamicData():
    """Return section Dynamic Data."""
    return render_template("dynamic_data.html")

@app.route("/about")
def about():
    """Return section About us."""
    return render_template("aboutus.html")

@app.route("/data")
def data():
    """Return section data."""
    return render_template("data.html")

@app.route("/caseStudies")
def caseStudies():
    """Return section Case studies."""
    return render_template("case_studies.html")

@app.route("/algorithm")
def algorithm():
    """Return section Case studies."""
    return render_template("algorithm.html")

@app.route("/capitalSearch")
def capitalSearch():
    """Return section Case studies."""
    return render_template("company_search.html")
###############################################

@app.route("/case_studies", methods=['GET', 'POST'])
def case_studies():
    """Return a list of sample names."""

    # Use Pandas to perform the sql query
    #stmt = db.session.query(Samples).statement
    #df = pd.read_sql_query(stmt, db.session.bind)

    # Return a list of the column names (sample names)
    #return jsonify(list(df.columns)[2:])
    return render_template("views/case_studies.html")


@app.route("/getData", methods=['GET'])
def getData():
    #myquery = { "Company Nation":"Brazil" }
    print(collection)
    data =list(collection.find())
    print(data)
    for elem in data:
        elem.pop('_id', None)

    response = jsonify(data)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

###search bar api######
@app.route("/searchCompany/<keywordData>", methods=['GET'])
def searchCompany(keywordData):
    company_list = []
    print(keywordData)
    data =list(collection.find({'Company Name':{'$regex':'^'+keywordData, '$options':"i"}}))
    print(data)
    for elem in data:
        company_list.append(elem['Company Name'])

    print(company_list)
    response = jsonify(company_list)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
############GET DATA FROM SEARCH ############
@app.route("/searchCompanyData/<wordSearch>", methods=['GET'])
def searchCompanyData(wordSearch):
    #company_list = []
    #print(keywordData)
    data =list(collection.find({'Company Name':wordSearch}))
    #print(data)
    for elem in data:
        #company_list.append(elem['Company Name'])
        elem.pop('_id', None)
    print(data)
    response = jsonify(data)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

##########################################

@app.route("/topFunding", methods=['GET'])
def topFunding():
    #myquery = { "Company Nation":"Brazil" }
    data =list(collection.find())
    for elem in data:
        elem.pop('_id', None)
        elem.pop('All Investor Firms', None)
        elem.pop('Company / Real Estate', None)
        elem.pop('Company Business Description', None)
        elem.pop('CSIC Description', None)
        elem.pop('Company Street Address, Line 1', None)
        elem.pop('Company Zip Code', None)
        elem.pop('Current Investor Firms', None)
        elem.pop('Gross Profit (USD) Mil', None)
        elem.pop('Last Investment Date', None)
        elem.pop('NAIC Description', None)
        elem.pop('Return on Equity', None)
        elem.pop('Revenue / Net Sales (USD) Mil', None)
        elem.pop('Statement Date', None)
        elem["Company Name"] = elem.pop('Company Name', None)
        try:
            elem["Total Funding To Date (USD) Mil"] = float(elem["Total Funding To Date (USD) Mil"])
        except:
            elem["Total Funding To Date (USD) Mil"] = 0

    data = sorted(data, key= lambda x: x["Total Funding To Date (USD) Mil"], reverse=True)
    response = jsonify(data)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route("/topFundingByCountry", methods=['GET'])
def topFundingByCountry():
    #myquery = { "Company Nation":"Brazil" }
    data =list(collection.find())
    for elem in data:
        elem.pop('_id', None)
        elem.pop('All Investor Firms', None)
        elem.pop('Company / Real Estate', None)
        elem.pop('Company Business Description', None)
        elem.pop('CSIC Description', None)
        elem.pop('Company Street Address, Line 1', None)
        elem.pop('Company Zip Code', None)
        elem.pop('Current Investor Firms', None)
        elem.pop('Gross Profit (USD) Mil', None)
        elem.pop('Last Investment Date', None)
        elem.pop('NAIC Description', None)
        elem.pop('Return on Equity', None)
        elem.pop('Revenue / Net Sales (USD) Mil', None)
        elem.pop('Statement Date', None)
        elem["Company Name"] = elem.pop('Company Name', None)
        try:
            elem["Total Funding To Date (USD) Mil"] = float(elem["Total Funding To Date (USD) Mil"])
        except:
            elem["Total Funding To Date (USD) Mil"] = 0

    total_country = {}
    for elem in data:
        key_val = elem["Company Nation"]
        if key_val in total_country.keys():
            total_country[key_val] += float(elem["Total Funding To Date (USD) Mil"])
        else:
            total_country[key_val] = float(elem["Total Funding To Date (USD) Mil"])

    list_country = []
    for key in total_country.keys():
        list_country.append({"Country": key , "Funding": total_country[key]})

    list_country = sorted(list_country, key= lambda x: x["Funding"], reverse=True)
    response = jsonify(list_country)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route("/FundingByYearCountry", methods=['GET'])
def FundingByYearCountry():
    #myquery = { "Company Nation":"Brazil" }
    data =list(collection.find())
    for elem in data:
        elem.pop('_id', None)
        elem.pop('All Investor Firms', None)
        elem.pop('Company / Real Estate', None)
        elem.pop('Company Business Description', None)
        elem.pop('CSIC Description', None)
        elem.pop('Company Street Address, Line 1', None)
        elem.pop('Company Zip Code', None)
        elem.pop('Current Investor Firms', None)
        elem.pop('Gross Profit (USD) Mil', None)
        elem.pop('Last Investment Date', None)
        elem.pop('NAIC Description', None)
        elem.pop('Return on Equity', None)
        elem.pop('Revenue / Net Sales (USD) Mil', None)
        elem.pop('Statement Date', None)
        try:
            elem["Funding Year"] = elem["Company Founded Date"].split('/')[2]
        except:
            elem["Funding Year"] = '0'
        elem.pop('Company Founded Date', None)
        elem["Company Name"] = elem.pop('Company Name', None)
        try:
            elem["Total Funding To Date (USD) Mil"] = float(elem["Total Funding To Date (USD) Mil"])
        except:
            elem["Total Funding To Date (USD) Mil"] = 0

    countries = []
    for elem in data:
        country = elem["Company Nation"]
        if country not in countries:
            countries.append(country)

    years_list = []
    for elem in data:
        year = elem["Funding Year"]
        if year not in years_list:
            years_list.append(year)

    country_year_dict = {}
    def returnYearDict(years_list):
        dict = {}
        for year in years_list:
            dict[year] = 0
        return dict

    for cou in countries:
        country_year_dict[cou] = returnYearDict(years_list)


    for coun in country_year_dict.keys():
        for elem in data:
            year = elem["Funding Year"]
            country = elem["Company Nation"]

            if coun == country:
                if year in country_year_dict[coun]:
                    country_year_dict[coun][year] += float(elem["Total Funding To Date (USD) Mil"])

    country_year_list = []
    for c in country_year_dict.keys():
        country_year_list.append({'country': c, 'data_by_year' :country_year_dict[c]})

    response = jsonify(country_year_list)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route("/FundingByYear", methods=['GET'])
def FundingByYear():
    #myquery = { "Company Nation":"Brazil" }
    data =list(collection.find())
    for elem in data:
        elem.pop('_id', None)
        elem.pop('All Investor Firms', None)
        elem.pop('Company / Real Estate', None)
        elem.pop('Company Business Description', None)
        elem.pop('CSIC Description', None)
        elem.pop('Company Street Address, Line 1', None)
        elem.pop('Company Zip Code', None)
        elem.pop('Current Investor Firms', None)
        elem.pop('Gross Profit (USD) Mil', None)
        elem.pop('Last Investment Date', None)
        elem.pop('NAIC Description', None)
        elem.pop('Return on Equity', None)
        elem.pop('Revenue / Net Sales (USD) Mil', None)
        elem.pop('Statement Date', None)
        try:
            elem["Funding Year"] = elem["Company Founded Date"].split('/')[2]
        except:
            elem["Funding Year"] = '0'
        elem.pop('Company Founded Date', None)
        elem["Company Name"] = elem.pop('Company Name', None)
        try:
            elem["Total Funding To Date (USD) Mil"] = float(elem["Total Funding To Date (USD) Mil"])
        except:
            elem["Total Funding To Date (USD) Mil"] = 0



    year_dict = {}
    for elem in data:
        key_val = elem["Funding Year"]
        if key_val in year_dict.keys():
            year_dict[key_val] += float(elem["Total Funding To Date (USD) Mil"])
        else:
            year_dict[key_val] = float(elem["Total Funding To Date (USD) Mil"])

    year_list = []
    for key in year_dict.keys():
        year_list.append({'year': key, 'total': year_dict[key] })


    year_list = sorted(year_list, key= lambda x: x["year"], reverse=True)
    response = jsonify(year_list)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


#@app.route("/samples/<sample>")
#def samples(sample):
#    """Return `otu_ids`, `otu_labels`,and `sample_values`."""
#    stmt = db.session.query(Samples).statement
#    df = pd.read_sql_query(stmt, db.session.bind)

    # Filter the data based on the sample number and
    # only keep rows with values above 1
#    sample_data = df.loc[df[sample] > 1, ["otu_id", "otu_label", sample]]
    # Format the data to send as json
#    data = {
#        "otu_ids": sample_data.otu_id.values.tolist(),
#        "sample_values": sample_data[sample].values.tolist(),
#        "otu_labels": sample_data.otu_label.tolist(),
#    }
#    return jsonify(data)


if __name__ == "__main__":
    app.run()
