docker_build:
	docker build . -t ball-plate

docker_run:
	xhost +
	sudo docker run  -it  -e DISPLAY=$$DISPLAY  -v /tmp/.X11-unix:/tmp/.X11-unix  --device /dev/video0  --device /dev/ttyACM0 ball-plate
#Con xhost + le damos permisos al docker para poder levantar una interfaz grafica
#con -it nos da una consola interactiva como cualquier PC con linux
#Con -e DISPLAY=$$DISPLAY le pasamos al docker la variable de entorno para la pantalla asi puede usar una GUI
#Con -v /tmp/.X11-unix:/tmp/.X11-unix  tambien esta relaciona con la gui
#con --device /dev/video0 le damos acceso al device de video para la GUI
#con --device /dev/ttyACM0 le damos acceso al puerto serie (tiene que estar conectado antes de hacer docker run sino va a dar error)
#ball-plate es el nombre del docker


#sin serial:
docker_run_test:
	xhost +
	sudo docker run  -it  -e DISPLAY=$$DISPLAY  -v /tmp/.X11-unix:/tmp/.X11-unix  --device /dev/video0 ball-plate
#Con xhost + le damos permisos al docker para poder levantar una interfaz grafica
#con -it nos da una consola interactiva como cualquier PC con linux
#Con -e DISPLAY=$$DISPLAY le pasamos al docker la variable de entorno para la pantalla asi puede usar una GUI
#Con -v /tmp/.X11-unix:/tmp/.X11-unix  tambien esta relaciona con la gui
#con --device /dev/video0 le damos acceso al device de video para la GUI
#con --device /dev/ttyACM0 le damos acceso al puerto serie (tiene que estar conectado antes de hacer docker run sino va a dar error)
#ball-plate es el nombre del docker