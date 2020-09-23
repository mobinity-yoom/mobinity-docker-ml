# tensorflow serving base imge
FROM tensorflow/serving:latest-gpu

# Sagemaker에서 TF Serving으로 추론을 리버스 프록시하는 역할인 NGINX 설치
RUN apt-get update
RUN apt-get install -y --no-install-recommends nginx git

# 모델폴더 컨테이너로 복사
COPY saved_model /saved_model

# NGINX 설정파일 컨테이너로 복사
COPY nginx.conf /etc/nginx/nginx.conf

#  NGNIX와 TF Serving 실행
ENTRYPOINT service nginx start | tensorflow_model_server --rest_api_port=8501 \
 --model_name=serving \
 --model_base_path=/saved_model