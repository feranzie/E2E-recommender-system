import json

import requests
from deepdiff import DeepDiff



url = "http://localhost:8080/2015-03-31/functions/function/invocations"
actual_response = requests.post(url, json=event).json()

print("actual response:")

print(json.dumps(actual_response, indent=2))

expected_response = {
    "predictions": ['Fashion Portfoilio', 'Fashion Design', 'Watercolours', 'Drawings', 'Sketch Video', 'Political Science', 'Colonialism In India', 'Legal Studies', 'Labor Law', 'Banking'],
        }
    

diff = DeepDiff(actual_response, expected_response, significant_digits=1)
print(f"diff={diff}")

assert "type_changes" not in diff
assert "values_changed" not in diff
