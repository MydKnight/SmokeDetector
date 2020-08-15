# SmokeDetector

## Troubleshooting Operations
When the PI starts up, the system service should run the app. There are ways to start, restart, stop and get the running status. They are:
* sudosystemctl start smokefrontend: Starts the service
* sudosystemctl stop smokefrontend: Stops the service
* sudosystemctl restart smokefrontend: Restarts the service
* sudosystemctl status smokefrontend: Gets the last several lines of output. Ctrl+c to break out

In order to get running output youll need to stop per the above and run sudo python3 app.py from the SmokeFrontend directory. This will cause constant output from the server side functions. 
