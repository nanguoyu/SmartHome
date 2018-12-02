echo "initalize camera"
echo "you can visit /mnt/usb/image/"
sudo modprobe bcm2835-v4l2
mjpg_streamer -i "input_uvc.so" -o "output_http.so -p 8090"