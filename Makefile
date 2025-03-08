all:
	mkdir -p ./lib && cd ./lib && cc -fPIC -shared -o rotate.so ../src/rotate.c

clean:
	rm ./lib/rotate.so
