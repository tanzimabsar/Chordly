from flask import Flask
from flask import jsonify, request
from harmony import progression
from harmony import chord
from marshmallow import Schema, fields
import random

app = Flask(__name__)


class ChordSchema(Schema):
    root = fields.Str()
    quality = fields.Str()
    notes = fields.List(fields.Str(),
        attribute='readable_notes')


class ProgressionSchema(Schema):
    name = fields.Str()
    key_center = fields.Str()
    chords = fields.Nested(ChordSchema())


@app.route('/chords', methods=['GET'])
def generate_chords():
    """ Import Random Character from selection of characters """
    root = request.args.get('root')
    scale = request.args.get('scale')
    length = int(request.args.get('length'))

    if not root:
        return jsonify({'error_message': "Please supply a root note."})
    if length is None:
        return jsonify({'error_message':'Supply length greater than 1'})

    prog = progression.Progression().generate_chords_in_scale(root.upper(),
        scale)

    chords = progression.Progression().filter(prog, 
        random.sample(range(0, 11), length))

    schema = ChordSchema(many=True)
    result = schema.dump(chords)

    return jsonify({'chords': result})


if __name__ == '__main__':
    app.run(debug=True)
