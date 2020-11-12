NUM_CPUS=$(shell grep -c processor /proc/cpuinfo)

install_system_deps:
	cat requirements.apt | xargs sudo apt install
activate_venv:
	poetry shell
run:
	@gunicorn \
	-w $(NUM_CPUS) \
	-b 0.0.0.0 \
	-k uvicorn.workers.UvicornWorker \
	--reload \
	wspython:app
services_up:
	docker-compose up -d
services_down:
	docker-compose down