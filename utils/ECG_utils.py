import json


raw_dataset_path="C:\\Users\\User\\Desktop\\ecg_data_200.json" #файл с датасетом

def healthy(diagnos):
    is_heathy =True
    axis_ok = False
    rythm_ok = False
    for key in diagnos.keys():
        if key == 'electric_axis_normal':
            if diagnos[key] == True:
                axis_ok = True
                continue
        if key == 'regular_normosystole':
            if diagnos[key] == True:
                rythm_ok = True
                continue
        if diagnos[key] == True:
            is_heathy = False
            break
    return axis_ok and rythm_ok and is_heathy

def get_first_healthy_signal():
    with open(raw_dataset_path, 'r') as f:
        data = json.load(f)

        for case_id in data.keys():
            diag = data[case_id]['StructuredDiagnosisDoc']
            if healthy(diag):
                return get_signal_by_case_id(case_id, lead_name='i')
    return None

def get_mini_ECG():
    full_signal = get_first_healthy_signal()
    step = 1
    new_len = 120
    new_indexes = list(range(180,  len(full_signal), step))
    new_signal = list([full_signal[i] for i in new_indexes])
    return new_signal[0:new_len]


def get_signal_by_case_id(case_id, lead_name='i'):
    with open(raw_dataset_path, 'r') as f:
        data = json.load(f)
        leads = data[case_id]['Leads']
        signal = leads[lead_name]['Signal']
        return signal

if __name__ == "__main__":
    print(get_first_healthy_signal())
