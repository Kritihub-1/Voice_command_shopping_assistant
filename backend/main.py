import os
from app import create_app

app = create_app()

@app.route('/health', methods=['GET'])
def health_check():
    return {'status': 'ok'}, 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV', 'development') == 'development'
    app.run(debug=debug, host='0.0.0.0', port=port)
