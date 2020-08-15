# SmokeDetector

## Troubleshooting Operations
When the PI starts up, the system service should run the app. There are ways to start, restart, stop and get the running status. They are:
* sudo systemctl start smokefrontend: Starts the service
* sudo systemctl stop smokefrontend: Stops the service
* sudo systemctl restart smokefrontend: Restarts the service
* sudo systemctl status smokefrontend: Gets the last several lines of output. Ctrl+c to break out

In order to get running output youll need to stop per the above and run sudo python3 app.py from the SmokeFrontend directory. This will cause constant output from the server side functions. 
