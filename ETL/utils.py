import json
import numpy as np

def recursiveDict(dct, parent_keys = ''):
    lst_keys = list(dct.keys())
    keys_lst = []
    val_lst = []
    for key in lst_keys:
        if isinstance(dct[key], dict):

                keys, vals = recursiveDict(dct[key], parent_keys + '_' + key)
                keys_lst += keys
                val_lst += vals
            
        else:
            if len(parent_keys) == 0:
                keys_lst += [key]
            else:
                keys_lst += [parent_keys + '_' + key]

            val_lst += [json.dumps(dct[key], ensure_ascii=False)] 
       
    return keys_lst, val_lst

def recursiveVal(dct):
    lst_keys = list(dct.keys())
    val_lst = []
    for key in lst_keys:
        
        print(np.isnan(dct[key]))
        val_lst += [dct[key]] if not np.isnan(dct[key]) else 0
       
    return val_lst

def recursiveKey(dct, parent_keys = ''):
    lst_keys = list(dct.keys())
    keys_lst = []
    for key in lst_keys:
        if isinstance(dct[key], dict):
                keys = recursiveKey(dct[key], parent_keys + '_' + key)
                keys_lst += keys
            
        else:
            if len(parent_keys) == 0:
                keys_lst += [key]
            else:
                keys_lst += [parent_keys + '_' + key]
       
    return keys_lst


def getKeys(dictType_values_list):
    keys_list = []
    for value in dictType_values_list:
        keys_list += recursiveKey(value)

    return list(frozenset(keys_list))