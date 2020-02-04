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
        if type(text)==list:
            data='{"inputs":{' \
                 '"tokens_ids":' + repr(text) + '},"output_mode":"'+output_mode+'"}'
        elif type(text)==str:
            data = '{"inputs":"' + text + '","output_mode":"'+output_mode+'"}'
        else:
            raise (TypeError,"current input type not supported")
    elif mode == 'tokenize':
        data = '{"text_input":"' + text +'",'+ '"return_ids":"True"'+'}'
    elif mode == 'detokenize':
        if type(text) == list:
            text=repr(text)
        data='{"tokens_ids":'+text+'}'
    response = requests.post('http://{}:{}/{}'.format(host, port,mode), headers=headers, data=data.encode('utf-8'))
    return json.loads(response.content)




def test_pack():
    host='localhost'
    port=8897
    text="something good"
    """
    res = transformers_res(text, mode='forward',output_mode='sum4layers', host=host, port=port)
    forward_res_1 = json.loads(res.content)
    res=transformers_res(text,mode='forward',output_mode='cat4layers',host=host,port=port)
    forward_res_2 = json.loads(res.content)
    """
    res = transformers_res([101, 1996, 3078, 5770, 1997, 5310, 1011, 8857, 2640, 2003, 2008, 1010, 2043, 2864, 2092, 1010, 2009, 21312, 2008, 1996, 4031, 2003, 6179, 1010, 24013, 1010, 1998, 15902, 2000, 1996, 2203, 1011, 5310, 1012, 102], mode='forward',output_mode='base', host=host, port=port)
    forward_res_3 = json.loads(res.content)
    print("HO")
    res=transformers_res(text,mode='tokenize',host=host,port=port)
    tokenize_res_1=json.loads(res.content)
    tokens_ids=tokenize_res_1['tokens_ids']
    res = transformers_res(tokens_ids, mode='detokenize', host=host, port=port)
    tokenize_res_2 = json.loads(res.content)
    #array_result = np.array(j_res['output'][0][output_pos][:])
    print("Hey there")


if __name__ == "__main__":
    test_pack()



