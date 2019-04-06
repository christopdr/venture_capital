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

@app.route("/topFunding", methods=['GET'])
def topFunding():
    top =collection.find({}, {'_id':1,'Company Name': 1, 'Total Funding To Date (USD) Mil':1})
    top_list = []
    for t in top:
        print(t)
        t.pop('_id', None)
        top_list.append(t)
    return jsonify(top_list)

@app.route("/getData", methods=['GET'])
def getData():
    myquery = { "Company Nation":"Brazil" }
    algo =list(collection.find(myquery))
    for elem in algo:
        elem.pop('_id', None)

    print(algo[:2])
    return jsonify(algo)

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
