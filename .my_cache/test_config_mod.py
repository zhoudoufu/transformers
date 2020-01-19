from transformers import  DistilBertTokenizer,DistilBertModel,DistilBertConfig
import torch

def main():
    model_name='distilbert-base-uncased'
    config_path="/Users/kouhuazhou/Documents/workplace/ThirdPartyTest/transformers/.my_cache/distilbert-pipeline-config.json"
    config=DistilBertConfig.from_pretrained(config_path)
    #config.output_hidden_states =True
    tok = DistilBertTokenizer.from_pretrained(model_name)
    model = DistilBertModel.from_pretrained(model_name,config=config)

    tok_res=tok.encode("something good")
    sentence = torch.tensor([tok_res])
    with torch.no_grad():
        output = model(sentence)
    sequence_output=output[0]
    ind=1
    # good config
    gconfig=DistilBertConfig.from_pretrained(model_name)
    #gconfig.output_hidden_states=True
    tok = DistilBertTokenizer.from_pretrained(model_name)
    gmodel= DistilBertModel.from_pretrained(model_name,config=gconfig)
    tok_res = tok.encode("something good")
    sentence = torch.tensor([tok_res])
    with torch.no_grad():
        goutput = gmodel(sentence)
    sequence_output = output[0]
    ind=2
    for attr, value in gconfig.__dict__.items():
        print(attr, value,getattr(config, attr))

if __name__ == '__main__':
    main()