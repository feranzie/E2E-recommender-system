from pathlib import Path

import model


def read_text(file):
    test_directory = Path(__file__).parent

    with open(test_directory / file, "rt", encoding="utf-8") as f_in:
        return f_in.read().strip()


#def test_base64_decode():
#    base64_input = read_text("data.b64")
##   actual_result = model.base64_decode(base64_input)
 #   expected_result =  ['Fashion Portfoilio', 'Fashion Design', 'Watercolours', 'Drawings', 'Sketch Video', 'Political Science', 'Colonialism In India', 'Legal Studies', 'Labor Law', 'Banking']
#
 #   assert actual_result == expected_result

class ModelMock:
    def __init__(self, value):
        self.value = value

    def predict(self, X):
        n = len(X)
        return [self.value] * n

def recommender():
    model_mock = ModelMock()
    model_service = model.ModelService(model_mock)

    user_id= '5df49b32cc709107827fb3c7'

    actual_prediction = model_service.predict(user_id)
    expected_prediction = ['Fashion Portfoilio', 'Fashion Design', 'Watercolours', 'Drawings', 'Sketch Video', 'Political Science', 'Colonialism In India', 'Legal Studies', 'Labor Law', 'Banking']

    assert actual_prediction == expected_prediction

"""def test_lambda_handler():
    model_mock = ModelMock()
    model_version = "Test123"

    base64_input = read_text("data.b64")

    event = {
        "Records": [
            {
                "kinesis": {
                    "data": base64_input,
                },
            }
        ]
    }

    actual_predictions = model_service.lambda_handler(event)
    expected_predictions = {
        "predictions": [
            {
                "model": "recommender_model",
                "version": model_version,
                "prediction": ['Fashion Portfoilio', 'Fashion Design', 'Watercolours', 'Drawings', 'Sketch Video', 'Political Science', 'Colonialism In India', 'Legal Studies', 'Labor Law', 'Banking'],
            }
        ]
    }

    assert actual_predictions == expected_predictions"""
