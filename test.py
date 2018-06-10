#Design a Flask app based on the queries in Climate Analysis

################################################
#Import dependencies
################################################
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func, text
from sqlalchemy.orm import query_expression

import os
from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)

#################################################
#Flask set-up
#################################################
app = Flask(__name__)

# create route that renders index.html template
@app.route("/")
def home():
    """Return the dashboard homepage."""
    return render_template("index2.html")

#################################################   
@app.route("/names")
def names():
    """List of sample names."""

    # Database Setup
    engine = create_engine("sqlite:///belly_button_biodiversity.sqlite")
    # reflect an existing database into a new model
    Base = automap_base()
    # reflect the tables
    Base.prepare(engine, reflect=True)

    # Map Samples class
    Samples = Base.classes.samples

    # create a session
    session = Session(engine)

    #Query database, get column names
    data = Samples.__table__.columns.keys()

    # Convert into list, then into JSON
    all_otu_ids = []
    for x in range(len(data)):
        if x > 0:
            name = str(data[x]).split(",")[0].split("[")[0]
            all_otu_ids.append(name)
        
    return jsonify(all_otu_ids)

################################################# 
@app.route("/otu")
def otu():
    """List of OTU descriptions."""
    # Database Setup
    engine = create_engine("sqlite:///belly_button_biodiversity.sqlite")
    # reflect an existing database into a new model
    Base = automap_base()
    # reflect the tables
    Base.prepare(engine, reflect=True)

    # Map Otu class
    Otu = Base.classes.otu

    # create a session
    session = Session(engine)

    #Query database
    data2 = session.query(Otu.lowest_taxonomic_unit_found).all() 

    # Convert into list, then into JSON
    all_otu_descriptions = []
    for x in range(len(data2)):
        description = str(data2[x]).split(",")[0].split("(")[1].split("'")[1]
        all_otu_descriptions.append(description)
    
    return jsonify(all_otu_descriptions)

############################################
@app.route("/metadata/<sample>")
def metadata(sample):
    """MetaData for a given sample."""

    # Database Setup
    engine = create_engine("sqlite:///belly_button_biodiversity.sqlite")
    # reflect an existing database into a new model
    Base = automap_base()
    # reflect the tables
    Base.prepare(engine, reflect=True)

    # Map Meta class
    Metadata = Base.classes.samples_metadata

    # get API input
    input_id = (sample)
    input_id_number = input_id.split("_")[1]

    # Prepare a variable for iterating
    Metadata_keys = Metadata.__table__.columns.keys()

    # Switch to SQL for a cleaner query than SQLAlchemy function provided

    # Raw SQL
    sql = text(f'SELECT * FROM samples_metadata WHERE (SAMPLEID = {input_id_number})')

    # Create connection and execute SQL
    connection = engine.connect()
    result = connection.execute(sql)

    # Convert list of tuples into a dictionary, then into JSON
    all_sample_data = []
    for row in result:
        # Create didctionary
        sample_dict = {}
        for x in range(len(row)):
            # Convert query return into keys and values
            sample_dict[Metadata_keys[x]] = row[x]

        # Append dictionary instance into list
        all_sample_data.append(sample_dict)
        
    #Close connection
    connection.close()

    #Convert to JSON
    return jsonify(all_sample_data)

######################################################
@app.route("/wfreq/<sample>")

def wash(sample):

    # get API input
    input_id = (sample)
    input_id_number = input_id.split("_")[1]

    #Database setup (would not run outside of def)
    engine = create_engine("sqlite:///belly_button_biodiversity.sqlite")

    # Use SQL for a cleaner query than SQLAlchemy function provided

    # Raw SQL
    sql2 = text(f'SELECT WFREQ FROM samples_metadata WHERE (SAMPLEID = {input_id_number})')
    # Create connection and execute SQL

    connection = engine.connect()
    result = connection.execute(sql2)

    # Convert returns to a list, then a dictionary, then into JSON
    wash_freq = []

    for row in result:
        wash_dict = {}
        wash_dict["wash_frequency"] = row[0]
        wash_freq.append(wash_dict)
        
    #Close connection
    connection.close()

    #Convert to JSON
    return jsonify(wash_freq)
    
#####################################################
@app.route("/samples/<sample>")

def samples(sample):

    # get API input
    input_id = (sample)
    input_id_number = input_id.split("_")[1]

    # Use SQL for a cleaner query than SQLAlchemy function provided

    # Raw SQL
    sql3 = text(f'SELECT otu_id, {input_id} FROM samples ORDER BY {input_id} DESC')

    # Database Setup
    engine = create_engine("sqlite:///belly_button_biodiversity.sqlite")

    # Create connection and execute SQL
    connection = engine.connect()
    result = connection.execute(sql3)

    # Convert returns to lists, then a dictionary, then into JSON
    all_otu_in_sample = []
    otu_ids = []
    sample_values = []

    for row in result:
        otu_ids.append(row[0])
        sample_values.append(row[1])
    
    # Create dictionary
    otu_dict = {}
    
    # Convert query return into keys and values
    otu_dict["otu_ids"] = otu_ids
    otu_dict["sample_values"] = sample_values
    
    # Append dictionary instance into list
    all_otu_in_sample.append(otu_dict)
        
    #Close connection
    connection.close()

    #Convert to JSON
    return jsonify(all_otu_in_sample)

if __name__ == "__main__":
    app.run(debug=True)