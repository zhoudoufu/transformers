import logging
from argparse import ArgumentParser
from typing import Any, List, Optional, Union

from transformers.pipelines import pipeline
try:
    from uvicorn import run
    from fastapi import FastAPI, HTTPException, Body
    from pydantic import BaseModel

    _serve_dependancies_installed = True
except (ImportError, AttributeError):
    BaseModel = object

    def Body(*x, **y):
        pass

    _serve_dependancies_installed = False


logger = logging.getLogger("transformers-cli/serving")


app_config={'task':'feature-extraction',
            'model':'distilbert-base-uncased',
            'config':'distilbert-pipeline-config.json',
            'tokenizer':'distilbert-base-uncased',
            'device':-1,
            'host':'localhost',
            'port':8897,
            'workers':8}


feat_pipeline=pipeline(
            task=app_config['task'],
            model=app_config['model'],
            config=app_config['config'],
            tokenizer=app_config['tokenizer'],
            device=app_config['device']
            )

class serving:
    @staticmethod
    def model_info():
        return ServeModelInfoResult(infos=vars(feat_pipeline.model.config))

    @staticmethod
    def tokenize( text_input: str = Body(None, embed=True), return_ids: bool = Body(False, embed=True)):
        """
        Tokenize the provided input and eventually returns corresponding tokens id:
        - **text_input**: String to tokenize
        - **return_ids**: Boolean flags indicating if the tokens have to be converted to their integer mapping.
        """
        try:
            tokens_txt = feat_pipeline.tokenizer.tokenize(text_input)

            if return_ids:
                tokens_ids = feat_pipeline.tokenizer.convert_tokens_to_ids(tokens_txt)
                return ServeTokenizeResult(tokens=tokens_txt, tokens_ids=tokens_ids)
            else:
                return ServeTokenizeResult(tokens=tokens_txt)

        except Exception as e:
            raise HTTPException(status_code=500, detail={"model": "", "error": str(e)})

    @staticmethod
    def detokenize(tokens_ids: List[int] = Body(None, embed=True),
        skip_special_tokens: bool = Body(False, embed=True),
        cleanup_tokenization_spaces: bool = Body(True, embed=True),
    ):
        """
        Detokenize the provided tokens ids to readable text:
        - **tokens_ids**: List of tokens ids
        - **skip_special_tokens**: Flag indicating to not try to decode special tokens
        - **cleanup_tokenization_spaces**: Flag indicating to remove all leading/trailing spaces and intermediate ones.
        """
        try:
            decoded_str = feat_pipeline.tokenizer.decode(tokens_ids, skip_special_tokens, cleanup_tokenization_spaces)
            return ServeDeTokenizeResult(model="", text=decoded_str)
        except Exception as e:
            raise HTTPException(status_code=500, detail={"model": "", "error": str(e)})

    @staticmethod
    def forward(inputs: Union[str, dict, List[str], List[int], List[dict]] = Body(None, embed=True),
        output_mode: str = Body(None, embed=True), output_pos: int = Body(None,embed=True)):
        """
        **inputs**:
        **attention_mask**:
        **tokens_type_ids**:
        """
        # Check we don't have empty string
        if len(inputs) == 0:
            return ServeForwardResult(output=[], attention=[])
        try:
            # Forward through the model
            output = feat_pipeline(inputs,output_mode,output_pos)
            return ServeForwardResult(output=output)
        except Exception as e:
            raise HTTPException(500, {"error": str(e)})


class ServeModelInfoResult(BaseModel):
    """
    Expose model information
    """

    infos: dict


class ServeTokenizeResult(BaseModel):
    """
    Tokenize result model
    """

    tokens: List[str]
    tokens_ids: Optional[List[int]]


class ServeDeTokenizeResult(BaseModel):
    """
    DeTokenize result model
    """

    text: str

class ServeForwardSumResult(BaseModel):
    """
    Forward result model
    """

    output: Any

class ServeForwardCatResult(BaseModel):
    """
    Forward result model
    """

    output: Any

class ServeForwardResult(BaseModel):
    """
    Forward result model
    """

    output: Any


app=FastAPI()
app.add_api_route("/", serving.model_info, response_model=ServeModelInfoResult, methods=["GET"])
app.add_api_route("/tokenize", serving.tokenize, response_model=ServeTokenizeResult, methods=["POST"])
app.add_api_route("/detokenize", serving.detokenize, response_model=ServeDeTokenizeResult, methods=["POST"])
app.add_api_route("/forward", serving.forward, response_model=ServeForwardResult, methods=["POST"])


if __name__ == "__main__":
    parser = ArgumentParser(description='Configure on host port and workers')
    parser.add_argument('--host', dest='host', default=app_config['host'],
                        help='host name for the serving')
    parser.add_argument('--port', dest='port', default=app_config['port'],type=int,
                        help='host port for the serving')
    parser.add_argument('--workers', dest='workers',type=int,
                        default=app_config['workers'],
                        help='multiprocess workers')

    args = parser.parse_args()
    run('mod_serving_multi:app', host=args.host, port=args.port, workers=args.workers,reload=False)
    print("App serving finished")


