import csv
from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

def identify_disease_from_symptom(symptom: str, sym_file: str, dis_file: str, symdis_file: str) -> str:
    # Read symptom data from sym.csv
    symptom_id = ""
    with open(sym_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) >= 2 and row[1] == symptom:
                symptom_id = row[0]
                break
    
    # Read disease data from dis.csv
    disease_name = ""
    with open(dis_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) >= 2 and row[0] == symptom_id:
                disease_id = row[1]
                break
    
    # Read symptom-disease mapping data from symdis.csv
    with open(symdis_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) >= 2 and row[0] == symptom_id:
                disease_id = row[1]
                break
    
    # Retrieve disease name from disease ID
    with open(dis_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) >= 2 and row[0] == disease_id:
                disease_name = row[1]
                break
    
    return disease_name


class ActionIdentifyDiseaseFromSymptom(Action):
    def name(self) -> Text:
        return "action_identify_disease_from_symptom"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        symptom = tracker.get_slot('symptom')
        sym_file = r"C:\Users\AMRITHA R J\Downloads\Rasa-Chatbot-master\Rasa-Chatbot-master\sym.csv"          # Replace with the path to your sym.csv file
        dis_file = r"C:\Users\AMRITHA R J\Downloads\Rasa-Chatbot-master\Rasa-Chatbot-master\dia_t.csv"          # Replace with the path to your dis.csv file
        symdis_file = r"C:\Users\AMRITHA R J\Downloads\Rasa-Chatbot-master\Rasa-Chatbot-master\diffsydiw.csv"    # Replace with the path to your symdis.csv file
        
        disease_name = identify_disease_from_symptom(symptom, sym_file, dis_file, symdis_file)
        disease_name = disease_name.replace(""," or ")
        if disease_name:
            response = f"Disease associated with symptom '{symptom}': {disease_name}"
        else:
            response = f"No disease found for symptom '{symptom}'."
        
        dispatcher.utter_message(text=response)
        
        return []
