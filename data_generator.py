from config import *

import random


# generate data

def generate_info(id, type_range, flow, available_rate):
    info = {
        'id': id,
        'type': random.randint(type_range[0], type_range[1]),
        'flow': flow,
        'available_shift': [],
    }
    for j in range(21):
        if random.random() < available_rate:
            info['available_shift'].append(j)
    return info


def generate_data():
    patients = []
    for i in range(random.randint(range_patient[0], range_patient[1])):
        patients.append(generate_info(i, (0, len(illness_name) - 1), max_flow['illness'], available_rate_patient))

    operators = []
    for i in range(random.randint(range_operator[0], range_operator[1])):
        operators.append(generate_info(i, (0, len(operator_category) - 1), max_flow['operator'], available_rate_operator))

    rooms = []
    for i in range(random.randint(range_room[0], range_room[1])):
        rooms.append(generate_info(i, (0, len(room_category) - 1), max_flow['room'], available_rate_room))

    anesthetists = []
    for i in range(random.randint(range_anesthesiologist[0], range_anesthesiologist[1])):
        anesthetists.append(generate_info(i, (0, len(anesthesiologist_category) - 1), max_flow['anesthesiologist'],
                                          available_rate_anesthesiologist))

    nurses = []
    for i in range(random.randint(range_nurse[0], range_nurse[1])):
        nurses.append(generate_info(i, (0, len(nurse_category) - 1), max_flow['nurse'], available_rate_nurse))

    # merge data
    resource = {
        'illness': patients,
        'operator': operators,
        'room': rooms,
        'anesthesiologist': anesthetists,
        'nurse': nurses,
    }
    return resource


# calculate n_patient:n_operator:n_room:n_anesthetist:n_nurse
def calculate_max_serving_flow(resource):
    max_serving_flow = 0
    for i in range(len(resource)):
        max_serving_flow += resource[i]['available_shift'].count(0) * resource[i]['flow']
    return max_serving_flow


# print abstract of generated data
def print_data_abstract(resource):
    print('================================================')
    for category, resources in resource.items():
        if category == 'illness':
            print(f'number of {category}: {len(resources)}')
            continue
        print(f'number of {category}: {len(resources)}')
    print('================================================\n')



if __name__ == '__main__':
    generate_data()