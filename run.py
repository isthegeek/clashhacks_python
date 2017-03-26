from flask import Flask, render_template, request, url_for
import finocial_pb2
import hashlib
import requests

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

@app.route('/hashmrz', methods=['POST'])
def hashmrz():
    passport_mrz = request.form['mrz']
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
    return hex_dig

@app.route('/submitpassporttochain', methods=['POST'])
def submitpassporttochain():
    passport_mrz = request.form['passport']
    public_key = request.form['public_key']
    signature = request.form['signature']
    mutation = finocial_pb2.Mutation()
    mutation.namespace = bytes("namespace", encoding="utf-8")
    record = mutation.records.add()
    PromptForRecord(record)
    mutation.metadata = bytes(passport_mrz, encoding="utf-8")
    protomutate = mutation.SerializeToString()
    
    # Hex of the mutation
    hexmutated = ''.join(hex(ord(x))[2:] for x in str(protomutate))
    
    url = "http://app.finocial.org:8181/finocialchain/submit"
    payload = {"mutation":hexmutated,"signatures":[{"pub_key":public_key,"signature":signature}]}
    headers = {
        'content-type': "application/json",
        'authorization': "58d57ea21fcdf300018ad5ecd3eccfc802124d8b705b2216f9aa087a",
        'accept': "application/vnd.travis-ci.2+json",
        'cache-control': "no-cache",
        'postman-token': "30fbfd63-775c-5e33-f11b-a325985e7471"
        }
    response = requests.request("POST", url, data=payload, headers=headers)
    print(response)
    return response.text

app.debug=True
app.run()








