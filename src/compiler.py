import io
import logging

cells: int = 30000


def _get_tab(n: int) -> str:
    return "    " * n


class BrainfuckCompiler:

    def __init__(self, stream: io.BufferedReader):
        self.stream: io.BufferedReader = stream
        self.output: io.StringIO = io.StringIO()

    def get_output(self) -> str:
        return self.output.getvalue()

    def _stream_back(self):
        self.stream.seek(-1, io.SEEK_CUR)

    def _group_read(self, char: bytes) -> int:
        n: int = 1
        while self.stream.read(1) == char:
            n += 1
        self._stream_back()
        return n

    def compile(self):
        self.output = io.StringIO()
        logging.debug("Compiling...")
        block_count: int = 0

        self.output.write(_get_tab(block_count) + "#include <stdio.h>\n")
        self.output.write(_get_tab(block_count) + "int main() {\n")
        block_count += 1
        self.output.write(_get_tab(block_count) + f"char cells[{cells}];\n")
        self.output.write(_get_tab(block_count) + "char *ptr = cells;\n")
        while (char := self.stream.read(1)) != b"":
            if char == b"+":
                group_size: int = self._group_read(b"+")
                logging.debug(f"Incrementing cell at {self.stream.tell()} of {group_size}")
                self.output.write(_get_tab(block_count) + f"*ptr += {group_size};\n")
            elif char == b"-":
                group_size: int = self._group_read(b"-")
                logging.debug(f"Decrementing cell at {self.stream.tell()} of {group_size}")
                self.output.write(_get_tab(block_count) + f"*ptr -= {group_size};\n")
            elif char == b">":
                group_size: int = self._group_read(b">")
                logging.debug(f"Incrementing pointer at {self.stream.tell()} of {group_size}")
                self.output.write(_get_tab(block_count) + f"ptr += {group_size};\n")
            elif char == b"<":
                group_size: int = self._group_read(b"<")
                logging.debug(f"Decrementing pointer at {self.stream.tell()} of {group_size}")
                self.output.write(_get_tab(block_count) + f"ptr -= {group_size};\n")
            elif char == b".":
                logging.debug(f"Printing cell at {self.stream.tell()}")
                self.output.write(_get_tab(block_count) + "putchar(*ptr);\n")
            elif char == b",":
                logging.debug(f"Reading cell at {self.stream.tell()}")
                self.output.write(_get_tab(block_count) + "*ptr = getchar();\n")
            elif char == b"[":
                logging.debug(f"Adding loop at {self.stream.tell()}")
                self.output.write(_get_tab(block_count) + "while (*ptr) {\n")
                block_count += 1
            elif char == b"]":
                logging.debug(f"Closing loop at {self.stream.tell()}")
                block_count -= 1
                self.output.write(_get_tab(block_count) + "}\n")

        if block_count != 1:
            raise Exception("Unbalanced brackets")
        self.output.write(_get_tab(block_count-1) + "}\n")
