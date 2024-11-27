from flask import Flask, request, jsonify, render_template, redirect, url_for
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

contacts = {}
contact_id_counter = 1

@app.route('/')
def index():
    return render_template('index.html', contacts=contacts.values())

@app.route('/contacts/new', methods=['GET', 'POST'])
def create_contact():
    global contact_id_counter
    if request.method == 'POST':
        data = request.form
        contact_id = contact_id_counter
        contacts[contact_id] = {
            "id": contact_id,
            "name": data['name'],
            "phone": data['phone'],
        }
        contact_id_counter += 1
        return redirect(url_for('index'))

    return render_template('create_contact.html')

@app.route('/contacts/<int:id>', methods=['GET'])
def get_contact(id):
    contact = contacts.get(id)
    if not contact:
        return jsonify({"message": "Contact not found"}), 404

    return render_template('contact.html', contact=contact)

@app.route('/contacts/<int:id>', methods=['POST'])
def delete_contact(id):
    if id not in contacts:
        return jsonify({"message": "Contact not found"}), 404

    del contacts[id]
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=False)
