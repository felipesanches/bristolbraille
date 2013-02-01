#manual
rm -f IMG_0003.JPG
shutter=25
aperture=4
echo shootmode
gphoto2 --set-config /main/capturesettings/shootingmode=3 --set-config /main/capturesettings/shutterspeed=$shutter --set-config /main/capturesettings/aperture=$aperture --set-config /main/capturesettings/focusingpoint=0 --set-config /main/capturesettings/afdistance=1 --capture-image #-and-download
