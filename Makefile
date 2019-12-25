all: build

build:
	docker image build --network host -t drl:latest .

run: build
	docker run --publish 8000:8080 --detach drl:latest python ./app.py

