from flask import *
from flask_restful import Api,Resource
from main import GenerateResponse
import waitress

app=Flask(__name__)
api=Api(app)

class SummarizeResource(Resource):
    def post(self):
        try:
            data=request.get_json()
            prompt=data['prompt']
            summary=GenerateResponse(prompt=prompt)
            return jsonify({"status":200,
                           "summary":summary})
        except Exception as e:
            return jsonify({"status":400,
                           "summary":""})
            print(e)
            
api.add_resource(SummarizeResource,'/prompt')
            
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
    # waitress.serve(app,port=80)