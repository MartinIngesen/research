import re, os


SOURCES = [
    "GET",
    "POST",
    "REQUEST",
    "SERVER['PHP",
    "SERVER['PATH_",
    "SERVER['REQUEST_U",
    "SERVER[\"PHP",
    "SERVER[\"PATH_",
    "SERVER[\"REQUEST_U"
]

SINKS = [
    "<?",
    "echo",
    "die",
    "print",
    "printf",
    "print_r",
    "var_dump",
]


def analyze(f):
    # Source variables
    svs = set()

    for i, line in enumerate(f):
        for source in SOURCES:
            if re.search(re.escape(f"$_{source}"), line):
                # Grab only the variable from this line
                v = line.split(" =")[0]

                # Check for direct <SINK> <SOURCE> calls
                direct = False
                for sink in SINKS:
                    if v.startswith(sink):
                        print(f"Direct source output found on line {i+1}: {v.rstrip()}")
                        direct = True

                if not direct:
                    svs.add(v)

    for i, line in enumerate(f):
        for sink in SINKS:
            for sv in svs:
                if re.search(re.escape(sink) + ".*" + re.escape(sv) + "([; \n])", line):
                    print(f"Tainted variable found on line {i+1}: {line.rstrip()}")
                    
    

if __name__ == "__main__":
    for root, _, files in os.walk("."):
        for f in files:
            path = os.path.join(root, f)
            if path.endswith(".php"):
                print(f"Analyzing {path}")
                analyze(open(path, "r").readlines())
                print("===")