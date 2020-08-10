
import serial, datetime, time, json

class GenerateControlSignal:
    def __init__(self, kValue=1, pValue=0, dValue=0, timeSample=3000, setPoint=5):
        self.iValue = kValue 
        self.pValue = pValue 
        self.dValue = dValue 
        self.timeSample = timeSample 
        self.setPoint = setPoint 
        self.lastTime = datetime.datetime.now()
        self.totalError = 0
        self.maxControl = 255
        self.minControl = 0
        self.deltaError = 0
        self.lastError = 0
        # Read the current selected Particles from config file 

        pass

    def calculateControlSignal():
        while True:
            # Calculate the average of the current selected particle readings. This is sensedOutput
            sensedOuput = getSensedOutput()

            error = self.setPoint - sensedOutput
            self.totalError += error
            
            # Total Error cannot be over the max DMX value or under the min. If so, set to the min/max value
            if self.totalError >= self.maxControl:
                self.totalError = self.maxControl
            elif self.totalError <= self.minControl:
                self.totalError = self.minControl

            self.deltaError  = error - self.lastError

            # This if check seems to be duplicated above...why?
            controlSignal = self.kValue * error + (self.iValue*self.timeSample)*self.totalError + (self.dValue/self.timeSample) * self.deltaError
            if controlSignal <= self.maxControl:
                controlSignal = self.maxControl
            elif controlSignal <= self.minControl:
                controlSignal = self.minControl

            self.lastError = error
            time.sleep(self.timeSample)


    def getSensedOutput():
        return 3
        