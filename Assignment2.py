from flask import Flask
from flask import request
from flask import jsonify, abort
from transformers.pipelines import pipeline
import sqlite3
import os

# Create my flask app
app = Flask(__name__)


# Define a handler for the / path, which returns "Hello World"
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

# Define a handler for the /answer path, which
# processes a JSON payload with a question and
# context and returns an answer using a Hugging
# Face model.

@app.route("/models", methods=['GET','PUT','DELETE'])
def models():
    print("API CALL RECEIVED")
    #Connect to database
    conn = sqlite3.connect('model_answer_db.db')
    #Create a cursor
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    print("Current list of tables ",c.fetchall())
    #code for models
    if request.method == 'GET':
        #Return all models
        payload = fetch_model()
        return payload

    if request.method == 'PUT':
        #fetch arguments passed by request
        data = request.json
        print("Request received is ",data)
        r_name =  data['name']
        r_tokenizer = data['tokenizer']
        r_model = data['model']

        #Add a new model and return updated model list
        #c.execute("SELECT name FROM sqlite_master WHERE type='table';")
        #print(c.fetchall())
        c.execute("INSERT INTO models VALUES(?,?,?)",(r_name,r_tokenizer,r_model))
        conn.commit()
        conn.close()
        #Get updated list of models
        payload = fetch_model()
        return payload

    if request.method == 'DELETE':
        #print(request)
        # Code to delete the model received in the request
        del_model = request.args.get('model')
        print("Model to be deleted is-",del_model)
        c.execute("DELETE FROM models WHERE name = (?)", (del_model,))
        conn.commit()
        # # c.execute("Select * from models where name = (?)", (del_model,))
        # c.execute("Select * from models")
        # print(c.fetchall())
        conn.close()
        # Get updated list of models
        payload = fetch_model()
        return payload

    #Commit the db
    conn.commit()
    #Close connection
    conn.close()

def fetch_model ():
    # Return all models
    conn = sqlite3.connect('model_answer_db.db')
    c = conn.cursor()
    c.execute("Select * from models")
    fetched_models = c.fetchall()
    payload = []
    content = {}
    for results in fetched_models:
        content = {'name': results[0], 'tokenizer': results[1], 'model': results[2]}
        payload.append(content)
        content = {}
    return jsonify(payload)

@app.route("/answer", methods=['POST','GET'])
def answer():
    print("ANSWER.............")
    print(request.method)
    import time
    if request.method == 'POST':
        # Get the request body data
        print("API call receoved to answer")
        req_model = request.args.get('model')
        data = request.json
        req_question = data['question']
        req_context = data['context']
        print(data)
        print(req_model)
        #Connect to database
        conn = sqlite3.connect('model_answer_db.db')
        # Create a cursor
        c = conn.cursor()

        if req_model == None:
            print("No model specified in the request. Using default model")
            req_model = "distilbert-base-uncased-distilled-squad"
            req_tokenizer = "distilbert-base-uncased-distilled-squad"
            req_name = "distilbert-base-uncased-distilled-squad"
        else:
            # Get model from database. If model is not found, then give HTTP response error
            c.execute("Select * from models where name = (?)", (req_model,))
            fetched_model = c.fetchone()
            print(fetched_model)
            if fetched_model == None:
                print("Model not found in the database")
                abort(404, description="Model not found in the database. Please try with a different model")
            else:
                req_name = fetched_model[0]
                req_tokenizer = fetched_model[1]
                req_model = fetched_model[2]

        # Import model
        print("Answer using model - ",req_model)
        hg_comp = pipeline('question-answering', model=req_model, tokenizer=req_tokenizer)

        # Answer the answer
        answer = hg_comp({'question':req_question, 'context':req_context})['answer']
        print("")

        #Generate timestamp
        timestamp = int(time.time())
        print(timestamp)

        #Enter the answer in the answers table
        c.execute("INSERT INTO answers VALUES(?,?,?,?,?)", (timestamp, req_name, answer, req_question, req_context))

        # Commit the db
        conn.commit()
        # Close connection
        conn.close()
        # Create the response body.
        out = {
            "timestamp":timestamp,
            "model":req_model,
            "answer": answer,
            "question": data['question'],
            "context": data['context'],
        }

        return jsonify(out)

    if request.method == 'GET':
        req_model = request.args.get('model')
        req_start_time = request.args.get('start')
        req_end_time = request.args.get('end')
        conn = sqlite3.connect('model_answer_db.db')
        c = conn.cursor()
        if req_model == None:
            # Return all answers within the start and end timestamp
            c.execute("Select * from answers where timestamp BETWEEN (?) AND (?)",(req_start_time,req_end_time ))
            fetched_models = c.fetchall()
            payload = []
            content = {}
            for results in fetched_models:
                content = {'timestamp': results[0], 'model': results[1], 'answer': results[2],'question': results[3], 'context': results[4]}
                payload.append(content)
                content = {}
            out = jsonify(payload)
        else:
            # Return all answers within the start and end timestamp
            conn = sqlite3.connect('model_answer_db.db')
            c = conn.cursor()
            c.execute("Select * from answers where model = (?) AND (timestamp BETWEEN (?) AND (?))",(req_model,req_start_time,req_end_time ))
            fetched_models = c.fetchall()
            payload = []
            content = {}
            for results in fetched_models:
                content = {'timestamp': results[0], 'model': results[1], 'answer': results[2],'question': results[3], 'context': results[4]}
                payload.append(content)
                content = {}
            out = jsonify(payload)
        return out
        # Commit the db
        conn.commit()
        # Close connection
        conn.close()
    return "<p>Hello, World!</p>"

def main():
    print("Welcome to main function")
    # Connect to database
    conn = sqlite3.connect('model_answer_db.db')

    # Create a cursor
    c = conn.cursor()

    # Create a table
    c.execute("""CREATE TABLE IF NOT EXISTS models (
            name varchar(100), tokenizer varchar(100), model varchar(100)
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS answers (
            timestamp DateTime, model varchar(100), answer varchar(500), question varchar(500), context varchar(500)
    )""")

    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    print(c.fetchall())
    #commit and close
    conn.commit()
    conn.close()

# Run if running "python answer.py"
if __name__ == '__main__':
    # Run our Flask app and start listening for requests
    main()
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
