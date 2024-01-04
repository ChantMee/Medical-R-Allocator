# config
TOT_WEEKS = 2

first_class = 'illness'

range_patient = (75, 100)
range_operator = (3, 4)
range_anesthesiologist = (6, 10)
range_room = (6, 10)
range_nurse = (10, 13)

# test
range_patient = (75, 75)
range_operator = (3, 3)
range_anesthesiologist = (3, 3)
range_room = (4, 4)
range_nurse = (2, 2)

available_rate_patient = 1
available_rate_operator = 0.3
available_rate_anesthesiologist = 0.3
available_rate_room = 0.4
available_rate_nurse = 0.3

# test
available_rate_patient = 1
available_rate_operator = 0.7
available_rate_anesthesiologist = 0.8
available_rate_room = 0.7
available_rate_nurse = 0.5

max_flow = {
    'illness': 1,
    'operator': 1,
    'room': 1,
    'anesthesiologist': 1,
    'nurse': 6,
}

# resource category
illness_name = [
    'Coronary Artery Bypass Graft',
    'Valve Replacement',
    'Brain Tumor Removal',
    'Spinal Fusion',
    'Joint Replacement',
    'Fracture Repair',
    'Heart Defect Repair',
    'Inguinal Hernia Repair',
    'Gallbladder Removal',
    'Appendectomy',
]
illness_name2id = {name: id for id, name in enumerate(illness_name)}

operator_category = [
    'Cardiology',
    'Neurology',
    'Orthopedics',
    'Pediatrics',
    'Surgery',
]
operator_category2id = {name: id for id, name in enumerate(operator_category)}

room_category = [
    'Surgical Room',
    'Pediatrics',
]
room_category2id = {name: id for id, name in enumerate(room_category)}

anesthesiologist_category = [
    'Anesthesiologist',
]
anesthesiologist_category2id = {name: id for id, name in enumerate(anesthesiologist_category)}

nurse_category = [
    'Nurse',
]
nurse_category2id = {name: id for id, name in enumerate(nurse_category)}

## merge category
id2name = {
    'illness': illness_name,
    'operator': operator_category,
    'room': room_category,
    'anesthesiologist': anesthesiologist_category,
    'nurse': nurse_category,
}
name2id = {
    'illness': illness_name2id,
    'operator': operator_category2id,
    'room': room_category2id,
    'anesthesiologist': anesthesiologist_category2id,
    'nurse': nurse_category2id,
}



# dependency
resource_category_dependency = {
    'illness': 'operator',
    'operator': 'room',
    'room': 'anesthesiologist',
    'anesthesiologist': 'nurse',
    'nurse': 'END',
}

dependency_illness = {
    'Coronary Artery Bypass Graft': ['Cardiology'],
    'Valve Replacement': ['Cardiology'],
    'Brain Tumor Removal': ['Neurology'],
    'Spinal Fusion': ['Neurology', 'Orthopedics'],
    'Joint Replacement': ['Orthopedics'],
    'Fracture Repair': ['Orthopedics'],
    'Heart Defect Repair': ['Pediatrics'],
    'Inguinal Hernia Repair': ['Pediatrics'],
    'Gallbladder Removal': ['Surgery'],
    'Appendectomy': ['Surgery'],
}

dependency_operator = {
    'Cardiology': ['Surgical Room'],
    'Neurology': ['Surgical Room'],
    'Orthopedics': ['Surgical Room'],
    'Pediatrics': ['Pediatrics'],
    'Surgery': ['Surgical Room'],
}

dependency_room = {
    'Surgical Room': ['Anesthesiologist'],
    'Pediatrics': ['Anesthesiologist'],
}

dependency_anesthesiologist = {
    'Anesthesiologist': ['Nurse'],
}

dependency_nurse = {
    'Nurse': ['END'],
}

def transform_to_id(dependency, name):
    dependency_id = dict()
    for key, deps in dependency.items():
        key_id = name2id[name][key]
        deps_id = [name2id[resource_category_dependency[name]][dep] if dep != 'END' else -1 for dep in deps]
        dependency_id[key_id] = deps_id
    return dependency_id

# transform to id
dependency_illness_id = transform_to_id(dependency_illness, 'illness')
dependency_operator_id = transform_to_id(dependency_operator, 'operator')
dependency_room_id = transform_to_id(dependency_room, 'room')
dependency_anesthesiologist_id = transform_to_id(dependency_anesthesiologist, 'anesthesiologist')
dependency_nurse_id = transform_to_id(dependency_nurse, 'nurse')

# merge dependency
dependency = {
    'category': resource_category_dependency,
    'illness': dependency_illness,
    'operator': dependency_operator,
    'room': dependency_room,
    'anesthesiologist': dependency_anesthesiologist,
    'nurse': dependency_nurse,
}
