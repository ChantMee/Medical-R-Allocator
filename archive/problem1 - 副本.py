import time
import random

# config
max_patient = 100
max_specialty = 16
max_room = 10

# specialty
specialty_id2name = [
    'Cardiology', 
    'Neurology', 
    'Orthopedics', 
    'Pediatrics', 
    'Surgery', 
    'Anesthesiology',
    'Nurse',
]
specialty_name2id = {name: id for id, name in enumerate(specialty_id2name)}

# dependency
dependency_name = {
    'Cardiology': ['Anesthesiology'],
    'Neurology': ['Anesthesiology'],
    'Orthopedics': ['Anesthesiology'],
    'Pediatrics': ['Anesthesiology'],
    'Surgery': ['Anesthesiology'],
    'Anesthesiology': ['Nurse'],
    'Nurse': [],
}
dependency = {specialty_name2id[name]: [specialty_name2id[dep] for dep in deps] for name, deps in dependency_name.items()}

# find operators
in_degree = [0] * len(specialty_id2name)
for deps in dependency.values():
    for dep in deps:
        in_degree[dep] += 1
operators = []
for i in range(len(in_degree)):
    if in_degree[i] == 0:
        operators.append(i)

# max serving people
max_serving_name = {
    'Cardiology': 1,
    'Neurology': 1,
    'Orthopedics': 1,
    'Pediatrics': 1,
    'Surgery': 1,
    'Anesthesiology': 1,
    'Nurse': 5,
}
max_serving = {specialty_name2id[name]: max_serving_name[name] for name in max_serving_name}

# patients, operator, room, anesthesiologis
patients = []
for i in range(max_patient):
    operator = random.choice(operators)
    patients.append({
        'id': i,
        'operator': operator,
    })

# operators
operators = []
cur_operator_id = 0
for i in range(len(specialty_id2name)):
    for k in range(random.randint(0, max_specialty)):
        # 0: Monday Morning, 1: Monday Afternoon, 2: Monday Night,
        # 3: Tuesday Morning, 4: Tuesday Afternoon, 5: Tuesday Night,
        # 6: Wednesday Morning, 7: Wednesday Afternoon, 8: Wednesday Night,
        # ....
        # 18: Sunday Morning, 19: Sunday Afternoon, 20: Sunday Night
        shift_available = []
        for j in range(21):
            if random.random() < 0.3:
                shift_available.append(j)
        operators.append({
            'id': cur_operator_id,
            'specialty': i,
            'shift_available': shift_available,
        })
        cur_operator_id += 1

# rooms
rooms = []
cur_room_id = 0
