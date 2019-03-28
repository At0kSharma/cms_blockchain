from flask import render_template, request, jsonify
from app import app, bchain
from uuid import uuid4

blockclass=bchain.Blockchain()
@app.route('/', methods=["GET"])
def index():
    length=len(blockclass.chain)
    pre_block = blockclass.get_previous_block()
    pre_hash = pre_block["previous_hash"]
    timestamp = pre_block["timestamp"]
    proof = pre_block["proof"]

    return render_template("index.html", length_data=length, hash=pre_hash, time=timestamp, proof=proof)


@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {'chain': blockclass.chain,
                'length': len(blockclass.chain)}
    return jsonify(response), 200


@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = blockclass.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockclass.proof_of_work(previous_proof)
    previous_hash = blockclass.hash(previous_block)

    block = blockclass.create_block(proof, previous_hash)
    response = {'message': 'Congratulations, you just mined a block!',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash'],
                'transactions': block['transactions']}
    return jsonify(response), 200


@app.route('/is_valid', methods=['GET'])
def is_valid():
    is_valid = blockclass.is_chain_valid(blockclass.chain)
    if is_valid:
        response = {'message': 'All good. The Blockchain is valid.'}
    else:
        response = {
            'message': 'Houston, we have a problem. The Blockchain is not valid.'}
    return jsonify(response), 200


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
    index = blockclass.sign_up(user_id, name, address, email, phone)
    response = {'message': f'Your details will be added to Block {index}'}
    return jsonify(response), 201


@app.route('/product')
def product():
    return render_template('product.html')

@app.route('/product', methods=['POST'])
def product_id():
    product_name = request.form.get('pname')
    amount = request.form.get('amount')
    quantity = request.form.get('quantity')
    product_id = str(uuid4()).replace('-', '')
    index = blockclass.product_id(product_id, product_name, amount, quantity)
    response = {'message': f'The product details will be added to Block{index}'}
    return jsonify(response), 201


@app.route('/status')
def status():
    return render_template('status.html')

@app.route('/status', methods=['POST'])
def add_status():
    courier_id = request.form.get('courier')
    current_location = request.form.get('location')
    status = request.form.get('status')
    index = blockclass.add_status(courier_id, current_location, status)
    response = {'message': f'This transaction will be added to Block {index}'}
    return jsonify(response), 201


@app.route('/courier')
def courier():
    return render_template('courier.html')

@app.route('/courier', methods=['POST'])
def courier_id():
    sender_id = request.form.get('sender')
    receiver_id = request.form.get('receiver')
    product_id = request.form.get('product')
    shipment_id = str(uuid4()).replace('-', '')
    index = blockclass.coureir_id(shipment_id, sender_id, receiver_id, product_id)
    response = {
        'message': f'The Courier details will be added to the block{index}'}
    return jsonify(response), 200
