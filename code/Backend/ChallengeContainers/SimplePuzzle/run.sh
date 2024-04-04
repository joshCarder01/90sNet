#!/bin/bash

socat TCP-LISTEN:${PORT:-300},tcpwrap=script,reuseaddr,fork EXEC:'/home/SimplePuzzle',stderr,pty,rawer