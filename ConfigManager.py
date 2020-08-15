import os, configparser, datetime, glob, json

class ConfigManager:
    """Provides functions for reading and updating the config file for a given run
    """
    def __init__(self):
        # If there is no file in configs, create one
        if not os.listdir('./configs'):
            print("Creating Log")
            self.filename = './configs/' + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.ini' 
            self.config_settings = configparser.ConfigParser()
            self.config_settings['DEFAULT'] = {
                                 'PValue': '1',
                                 'IValue': '0',
                                 'DValue': '0',
                                 'SetPoint': '',
                                 'SelectedSizes': '00000',
                                 'Domain': '',
                                 'DomainValue': '0',
                                 'DomainMultiplier': '0',
                                 'SamplingInterval': '3',
                                 'ControlInterval': '180',
                                 'ControlValue': '1',
                                 'PumpChannel': '1',
                                 'FanChannel': '2',
                                 'FanSpeed': '255'}
            with open(self.filename, 'w') as configfile:
                self.config_settings.write(configfile)

        # If there is, grab the most recent one and use that as our config settings. 
        else:
            print("Updating Configs")
            configs = glob.glob('./configs/*') 
            self.filename = max(configs, key=os.path.getctime)
            self.config_settings = configparser.ConfigParser()
            
    def __del__(self):
        # Write back to JSON file in the configs directory
        pass

    def updateConfig(self, updateArray):
        """Given a JSON Array, update all values

        Args:
            updateArray ([string]): JSON Array of Key/Value Pairs
            
        """
        # Different parameters will be different datatypes. Verify that they are correct before updating
        self.config_settings.read(self.filename)
        settings = json.loads(updateArray)
        for key in settings.keys():
            self.config_settings.set("DEFAULT", key, str(settings[key]))
        with open(self.filename, 'w+') as configfile:
            self.config_settings.write(configfile)
        return self.config_settings

    def get_setting(self, setting=None):
        """Gets a given setting value for a passed key

        Args:
            setting (string, optional): The key the user wants to retrieve. Defaults to None.

        Returns:
            Variable: The value for the passed key
        """
        if setting==None:
            return
        else:
            self.config_settings.read(self.filename)
            return self.config_settings['DEFAULT'][setting]