
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import date

cred = credentials.Certificate("fantastic-4-17e97-firebase-adminsdk-bt1mc-455424f7ee.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
current_year = date.today().year
current_day = date.today()

# Create dummy data sample 
pipe_dummy_data1 = {
    'id': 'site1', 
    'material': 'steel', 
    'age': 10, 
    'diameter': 300, 
    'pressure': 1.1, 
    'depth': 0.7 , 
    'warranty': 30,
    'check-frequency': 2,
    'last-check-date': str(current_day),
    'total-detected-leak': 2,
    'year-of-manufacture': 2000
}

pipe_dummy_data2 = {
    'id': 'site2', 
    'material': 'Cast-iron', 
    'age': 7, 
    'diameter': 200, 
    'pressure': 0.6, 
    'depth': 0.5 , 
    'warranty': 30,
    'check-frequency': 1,
    'last-check-date': str(current_day),
    'total-detected-leak': 10,
    'year-of-manufacture': 2003
}

# Generate dummy data


# Generate today's data
db.collection('infrastructure').document(str(current_day)).collection('pipe').add(pipe_dummy_data1)
db.collection('infrastructure').document(str(current_day)).collection('pipe').add(pipe_dummy_data2)

# ref: https://www.sciencedirect.com/science/article/pii/S1875389212007602
def GreyRelational(D, H, P):
   """ Time Prediction Model for Pipeline Leakage Based on Grey Relational Analysis """
   Y = -1999.02*D+17318.428*H+450.949*P 
   return Y
 
# ref: https://digital.csic.es/bitstream/10261/167067/1/Leak-Bayesian.pdf
def BayesianClassifiers(freq, total_leak, age):
    pass

def predictToBeBroken(data):
    """Main algorithm: which combines serveral potenital algorithm"""
    # 1. Check if expired
    left_warranty_year = data.get('warranty') + data.get('year-of-manufacture') - current_year 
    if left_warranty_year == 0:
        return True 
    
    # 2. Predicted by Grey Relational Analysis
    grey_res = GreyRelational(data.get('diameter'), data.get('depth'), data.get('pressure'))
    if grey_res > 0:
        return True
    
    # 3. Bayesian classifiers
    baye = BayesianClassifiers(data.get('check-frequency'), data.get('total-detected-leak'), data.get('age'))
    
    
    
    
    return False

def runUpdates(today_pipe_data):
    """run the algorithm in every new pipe data today"""
    broken_sites = []
    for d in today_pipe_data:
        data = d.to_dict()
        if predictToBeBroken(data): 
            broken_sites.append(data.get('id')) 
    return broken_sites         

if __name__ == '__main__':
    # Check if there is today's new data
    today_pipe_data = db.collection('infrastructure').document(str(current_day)).collection('pipe').get()
    broken_sites = []
    if today_pipe_data:
        broken_sites = runUpdates(today_pipe_data)
        
    # If there is broken site predicted, add to today's scheduling database
    repair_data = {'emergency repair': True}
    for site in broken_sites:
        db.collection('Schedule').document(str(current_day)).collection('Pipeline').document(str(site)).add(repair_data)
    

        


