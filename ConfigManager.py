import os, configparser, datetime, glob

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
                                 'ControlValue': '1'}
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

    def updateConfig(self, updateSetting, updateValue):
        """Given a key/value pair, update the dataset with the new value

        Args:
            updateSetting ([string]): Key that the user wishes to update
            updateValue ([int/string]): The value the user wishes to update
        """
        # Different parameters will be different datatypes. Verify that they are correct before updating
        self.config_settings.read(self.filename)
        self.config_settings.set("DEFAULT", updateSetting, updateValue)
        with open(self.filename, 'w') as configfile:
            self.config_settings.write(configfile)

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