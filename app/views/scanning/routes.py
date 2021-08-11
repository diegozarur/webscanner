from flask import jsonify, abort, request
from app.views.scanning import blueprint
from app.views.scanning.tasks import Scanning


@blueprint.route('/search', methods=['GET'])
def search():
    if not 'page' in request.args and request.args:
        return jsonify({'success': False, 'message': "did you mean!?, ...?page=1"}), 400

    task_searching = Scanning()
    try:
        result = task_searching.delay(request_data={'page': request.args.get('page', 1)})
        return jsonify(
            {
                'state': result.state,
                'task_id': result.task_id,
                'url': f'http://localhost:5000/api/scanning/status/{result.task_id}'
            }
        ), 200
    except Exception as e:
        return jsonify({'success': False, 'message': "Something bad happened"}), 500


@blueprint.route("/status/<message_id>", methods=["GET"])
def searching_status(message_id):
    task_searching = Scanning()
    data = task_searching.AsyncResult(message_id)
    if data.state != 'FAILURE':
        return jsonify({
            'state': data.state,
            'result': data.result

        }), 200

    return jsonify({
        'state': data.state,
        'result': str(data.result)

    }), 500