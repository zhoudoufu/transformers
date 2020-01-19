import requests
import json


def transformers_res(text,mode='forward',host='localhost', output_mode='sum4layers',port=8888):
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }

    if mode in ['forward','','tokenize','detokenize']:
        pass
    elif output_mode in ['sum4layers','cat4layers','base']:
        pass
    else:
        raise ("Unsupported type of query.")
    if mode.startswith('forward'):
        data = '{"inputs":"' + text + '",'+'"output_mode":'+'"'+output_mode+'"'+'}'
    elif mode == 'tokenize':
        data = '{"text_input":"' + text +'",'+ '"return_ids":"True"'+'}'
    response = requests.post('http://{}:{}/{}'.format(host, port,mode), headers=headers, data=data.encode('utf-8'))
    return response

def test_pack():
    host='localhost'
    port=8888
    text="something good"
    res = transformers_res(text, mode='forward',output_mode='sum4layers', host=host, port=port)
    forward_res_1 = json.loads(res.content)
    res=transformers_res(text,mode='forward',output_mode='cat4layers',host=host,port=port)
    forward_res_2 = json.loads(res.content)
    res = transformers_res(text, mode='forward',output_mode='base', host=host, port=port)
    forward_res_3 = json.loads(res.content)
    res=transformers_res(text,mode='tokenize',host=host,port=port)
    tokenize_res=json.loads(res.content)
    #array_result = np.array(j_res['output'][0][output_pos][:])
    print("Hey there")


if __name__ == "__main__":
    test_pack()



