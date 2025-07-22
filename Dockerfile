FROM public.ecr.aws/lambda/python:3.12

COPY ./ ${LAMBDA_TASK_ROOT}
WORKDIR /app
copy . .
COPY ./requirments.txt ./requirments.txt
RUN pip install -r ./requirments.txt
CMD ["main.handler"]