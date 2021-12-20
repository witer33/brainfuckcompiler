import argparse
import logging
import os
from compiler import BrainfuckCompiler

os.system("")
logging_format = "\033[95m(%(asctime)s) \033[94m%(levelname)s: \033[0m%(message)s"
parser = argparse.ArgumentParser(description='Compile Brainfuck to C!')

parser.add_argument("--file", "-f", help="File to compile", required=True)
parser.add_argument("--output", "-o", help="Output file", default="out.exe" if os.name == "nt" else "out")
parser.add_argument("--debug", "-d", help="Debug mode", action="store_true")
parser.add_argument("--ccode", "-c", help="Output C code", action="store_true")
parser.add_argument("--run", "-r", help="Run compiled file", action="store_true")


if __name__ == "__main__":
    args = parser.parse_args()
    logging.basicConfig(format=logging_format, level=logging.DEBUG if args.debug else logging.INFO)
    logging.info(f"Starting compilation of {args.file}")
    compiler = BrainfuckCompiler(open(args.file, "rb"))
    logging.info("Generating C code")
    compiler.compile()
    if args.ccode:
        logging.info(f"Saving C code to {args.output}")
        open(args.output, "w").write(compiler.get_output())
    else:
        open(f"{args.file}.c", "w").write(compiler.get_output())
        logging.info("Compiling C code to executable")
        os.system(f"gcc -o {args.output} {args.file}.c")
        os.remove(f"{args.file}.c")
        if args.run:
            logging.info("Running compiled file")
            os.system(f"{args.output}")
    logging.info("Compilation finished")
