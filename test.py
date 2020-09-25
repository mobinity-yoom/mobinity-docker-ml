# 배포된 엔드포인트 로컬에서 테스트
import boto3
import json
import base64

sagemaker_client = boto3.client('sagemaker-runtime')

# 데이터 encode
filepath = './test.jpeg'
with open(filepath, "rb") as image:
  image_data = image.read()
  encoded_input_string = base64.b64encode(image_data).decode('utf-8')

data = json.dumps(
    {"signature_name": "serving_default", "instances": [{"inputs": {'b64': encoded_input_string}}]}
    )

# response 받기
json_response = sagemaker_client.invoke_endpoint(
        EndpointName='object-detection-v1-endpoint', # endpoint name
        ContentType='application/json',
        Body=data
        )
        
res_json = json.loads(json_response['Body'].read().decode("utf-8"))

# print (상위 5개)
predictions = res_json['predictions'][0]

detection_boxes = list(predictions['detection_boxes'])[:5]
detection_classes = list(predictions['detection_classes'])[:5]
detection_scores = list(predictions['detection_scores'])[:5]

results = {'detection_boxes': detection_boxes,
            'detection_classes': detection_classes,
            'detection_scores': detection_scores}

print(results)