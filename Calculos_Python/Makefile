docker_build:
	docker build . -t ball-plate

docker_run:
	xhost +
	sudo docker run  -it  -e DISPLAY=$$DISPLAY  -v /tmp/.X11-unix:/tmp/.X11-unix  --device /dev/video0  ball-plate
