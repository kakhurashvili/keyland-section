FROM python:alpine3.17

WORKDIR /usr/src/app
RUN pip install Django==4.2 whitenoise==6.4.0
COPY . .
RUN python src/manage.py collectstatic

ENTRYPOINT ["python"]
EXPOSE 8080
CMD ["src/manage.py", "runserver", "0.0.0.0:8080"]
