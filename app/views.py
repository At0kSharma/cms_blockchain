from flask import render_template, request, jsonify, url_for, redirect
from app import app, bchain
from uuid import uuid4
import json

blockclass=bchain.Blockchain()
@app.route('/')
@app.route('/dashboard')
def dashboard():
    blockclass.replace_chain()
    length=len(blockclass.chain)
    pre_block = blockclass.get_previous_block()
    pre_hash = pre_block["previous_hash"]
    timestamp = pre_block["timestamp"]
    proof = pre_block["proof"]

    return render_template("index.html", length_data=length, hash=pre_hash, time=timestamp, proof=proof)


@app.route('/get_chain', methods=['GET'])
def get_chain():
    blockclass.replace_chain()
    data=blockclass.chain
    return render_template('chain.html',data=data), 200

@app.route('/get_block', methods = ['GET'])
def get_block():
    response = {'chain': blockclass.chain,
                'length': len(blockclass.chain)}
    return jsonify(response), 200

@app.route('/mine_block', methods=['GET'])
def mine_block():
    blockclass.replace_chain()
    previous_block = blockclass.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockclass.proof_of_work(previous_proof)
    previous_hash = blockclass.hash(previous_block)

    blockclass.create_block(proof, previous_hash)
    return redirect(url_for('dashboard'))


@app.route('/is_valid', methods=['GET'])
def is_valid():
    is_valid = blockclass.is_chain_valid(blockclass.chain)
    if is_valid:
        response = {'message': 'All good. The Blockchain is valid.'}
    else:
        response = {
            'message': 'Houston, we have a problem. The Blockchain is not valid.'}
    return jsonify(response)


@app.route('/sign')
def sign():
    return render_template('sign_up.html')

@app.route('/sign', methods=['POST'])
def sign_up():
    name = request.form.get('name')
    address = request.form.get('address')
    email = request.form.get('email')
    phone = request.form.get('phone')
    user_id = str(uuid4()).replace('-', '')
    blockclass.sign_up(user_id, name, address, email, phone)
    return render_template('sign_up_cnf.html',user_id=user_id,name=name,address=address,email=email,phone=phone)

@app.route('/sign_cnf')
def sign_cnf():
    return redirect(url_for('mine_block'))

@app.route('/product')
def product():
    return render_template('product.html')

@app.route('/product', methods=['POST'])
def product_id():
    product_name = request.form.get('pname')
    amount = request.form.get('amount')
    quantity = request.form.get('quantity')
    product_id = str(uuid4()).replace('-', '')
    blockclass.product_id(product_id, product_name, amount, quantity)
    return render_template('product_cnf.html',product_id=product_id,pname=product_name,amt=amount,qty=quantity)

@app.route('/product_cnf')
def product_cnf():
    return redirect(url_for('mine_block'))

@app.route('/status')
def status():
    return render_template('update_status.html')

@app.route('/status', methods=['POST'])
def add_status():
    courier_id = request.form.get('courier')
    current_location = request.form.get('location')
    status = request.form.get('status')
    blockclass.add_status(courier_id, current_location, status)
    return redirect(url_for('mine_block'))

@app.route('/track')
def track():
    return render_template('track.html')

@app.route('/track', methods=["POST"])
def tracking():
    req = request.form.get('data')
    json=blockclass.chain
    return render_template('get_stat.html',req_data=req, data=json)

@app.route('/courier')
def courier():
    return render_template('courier.html')

@app.route('/courier', methods=['POST'])
def courier_id():
    sender = request.form.get('sender')
    receiver = request.form.get('receiver')
    product = request.form.get('product')
    shipment_id = str(uuid4()).replace('-', '')
    blockclass.coureir_id(shipment_id, sender, receiver, product)
    return render_template('courier_cnf.html',courier_id=shipment_id,sender=sender,receiver=receiver,product=product)

@app.route('/courier_cnf')
def courier_cnf():
    return redirect(url_for('mine_block'))

@app.route('/connect_node')
def connect():
    return render_template("connect.html")

@app.route('/connect_node', methods=['POST'])
def connect_node():
    json = {
        "nodes": [
            "http://127.0.0.1:5001"
        ]
    }
    nodes = json.get('nodes')
    if nodes is None:
        return "No node"
    for node in nodes:
        blockclass.add_node(node)
    return redirect(url_for('dashboard'))


@app.route('/update_chain')
def update_chain():
    blockclass.replace_chain()
    return redirect(url_for('dashboard'))


@app.route('/search_data')
def search():
    return render_template('search.html')

@app.route('/search_data', methods=["POST"])
def search_data():
    blockclass.replace_chain()
    json=blockclass.chain
    select = request.form.get('data')
    s_id=request.form.get('select')
    return render_template("detail.html", select=select, s_id=s_id, data=json)
