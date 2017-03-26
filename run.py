from flask import Flask, render_template, request, url_for
import finocial_pb2
import hashlib

app = Flask(__name__)

def PromptForRecordvalue(recordvalue):
  recordvalue.data = bytes("data", encoding="utf-8")

def PromptForRecord(record):
  record.key =  bytes("key", encoding="utf-8")
  PromptForRecordvalue(record.value)
  record.version = bytes("version", encoding="utf-8")


@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"


@app.route('/submitpassporttochain', methods=['POST'])
def login():
    passport_mrz = request.form['passport']
    mutation = finocial_pb2.Mutation()
    mutation.namespace = bytes("namespace", encoding="utf-8")
    record = mutation.records.add()
    PromptForRecord(record)
    mutation.metadata = bytes(passport_mrz, encoding="utf-8")
    protomutate = mutation.SerializeToString()
    
    # Hex of the mutation
    hexmutated = ''.join(hex(ord(x))[2:] for x in str(protomutate))
    
    # hash of the hex of mutation
    hash_object = hashlib.sha256(hexmutated.encode())
    hex_dig = hash_object.hexdigest()
    print(hex_dig)
    print("\n\n\n--------------\n\n\n")
    print(hash_object)
    return "hello"

app.debug=True
app.run()








