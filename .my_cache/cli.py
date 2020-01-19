# coding: utf8
from os.path import dirname,abspath
import sys
project_dir = dirname(dirname(abspath(__file__)))
sys.path.append(project_dir)
import uvicorn

class ServingAPP():
    def __init__(self,app_pipeline):
        self.app=app_pipeline


def main():
    import sys

    if len(sys.argv) < 2 or sys.argv[1] not in ["convert", "train", "predict", "serve"]:
        print(
            "First argument to `transformers` command line interface should be one of: \n"
            ">> convert serve train predict"
        )
    if sys.argv[1] == "convert":
        from transformers.commands import convert

        convert(sys.argv)
    elif sys.argv[1] == "train":
        from transformers.commands import train

        train(sys.argv)
    elif sys.argv[1] == "serve":
        from argparse import ArgumentParser
        #from transformers.commands.mod_serving import ServeCommand
        from src.transformers.commands.mod_serving import ServeCommand
        parser = ArgumentParser('Transformers CLI tool', usage='transformers serve <command> [<args>]')
        commands_parser = parser.add_subparsers(help='transformers-cli command helpers')

        # Register commands
        ServeCommand.register_subcommand(commands_parser)

        # Let's go
        args = parser.parse_args()

        if not hasattr(args, 'func'):
            parser.print_help()
            exit(1)
        # Run
        service = args.func(args)
        return service
        #service.run()


if __name__ == "__main__":
    service=main()
    app = ServingAPP(service._app)
    uvicorn.run("cli:app", host=service._host, port=service._port, workers=4)
    print("Hey")