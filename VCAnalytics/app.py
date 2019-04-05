import os

import pandas as pd
import numpy as np
import pymongo
import json
from flask import Flask, jsonify, render_template


app = Flask(__name__)

client = pymongo.MongoClient("mongodb+srv://adminUsr:mongo1234@venturecapital-mmycs.mongodb.net/admin?retryWrites=true")
db = client.VentureCapitalWW_db
collection = db.LATAMtb

app.config.update(
    JSON_AS_ASCII= True
)

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
    data =list(collection.find())
    for elem in data:
        elem.pop('_id', None)

    response = jsonify(data)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


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
        elem["Company Name"] = elem.pop('﻿Company Name', None)
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
        elem["Company Name"] = elem.pop('﻿Company Name', None)
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
    
    list_country = sorted(list_country, key= lambda x: x["Country"], reverse=True)
    response = jsonify(list_country)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route("/metadata/<sample>")
def sample_metadata(sample):
    """Return the MetaData for a given sample."""
    sel = [
        Samples_Metadata.sample,
        Samples_Metadata.ETHNICITY,
        Samples_Metadata.GENDER,
        Samples_Metadata.AGE,
        Samples_Metadata.LOCATION,
        Samples_Metadata.BBTYPE,
        Samples_Metadata.WFREQ,
    ]

    results = db.session.query(*sel).filter(Samples_Metadata.sample == sample).all()

    # Create a dictionary entry for each row of metadata information
    sample_metadata = {}
    for result in results:
        sample_metadata["sample"] = result[0]
        sample_metadata["ETHNICITY"] = result[1]
        sample_metadata["GENDER"] = result[2]
        sample_metadata["AGE"] = result[3]
        sample_metadata["LOCATION"] = result[4]
        sample_metadata["BBTYPE"] = result[5]
        sample_metadata["WFREQ"] = result[6]

    print(sample_metadata)
    return jsonify(sample_metadata)


@app.route("/samples/<sample>")
def samples(sample):
    """Return `otu_ids`, `otu_labels`,and `sample_values`."""
    stmt = db.session.query(Samples).statement
    df = pd.read_sql_query(stmt, db.session.bind)

    # Filter the data based on the sample number and
    # only keep rows with values above 1
    sample_data = df.loc[df[sample] > 1, ["otu_id", "otu_label", sample]]
    # Format the data to send as json
    data = {
        "otu_ids": sample_data.otu_id.values.tolist(),
        "sample_values": sample_data[sample].values.tolist(),
        "otu_labels": sample_data.otu_label.tolist(),
    }
    return jsonify(data)


if __name__ == "__main__":
    app.run()
