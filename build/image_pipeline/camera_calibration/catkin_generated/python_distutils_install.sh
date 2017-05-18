#!/bin/sh

if [ -n "$DESTDIR" ] ; then
    case $DESTDIR in
        /*) # ok
            ;;
        *)
            /bin/echo "DESTDIR argument must be absolute... "
            /bin/echo "otherwise python's distutils will bork things."
            exit 1
    esac
    DESTDIR_ARG="--root=$DESTDIR"
fi

echo_and_run() { echo "+ $@" ; "$@" ; }

echo_and_run cd "/home/templerobotics/ros-nuc/src/image_pipeline/camera_calibration"

# snsure that Python install destination exists
echo_and_run mkdir -p "$DESTDIR/home/templerobotics/ros-nuc/install/lib/python2.7/dist-packages"

# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
echo_and_run /usr/bin/env \
    PYTHONPATH="/home/templerobotics/ros-nuc/install/lib/python2.7/dist-packages:/home/templerobotics/ros-nuc/build/lib/python2.7/dist-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/home/templerobotics/ros-nuc/build" \
    "/usr/bin/python" \
    "/home/templerobotics/ros-nuc/src/image_pipeline/camera_calibration/setup.py" \
    build --build-base "/home/templerobotics/ros-nuc/build/image_pipeline/camera_calibration" \
    install \
    $DESTDIR_ARG \
    --install-layout=deb --prefix="/home/templerobotics/ros-nuc/install" --install-scripts="/home/templerobotics/ros-nuc/install/bin"
