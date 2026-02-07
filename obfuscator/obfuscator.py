import argparse
import base64
import marshal
import zlib
import sys
import time
import random
from pathlib import Path

def print_banner():
    banner = """
  .----------------------------------------------------------------------.
  |_.-._.-._.-._.-._.-._.-.    _.-._.-._.-.    _.-._.-._.-._.-._.-._.-._.|
  |_.-._.-._.-._.-._.-._. .::db .-._.-._. .::db .-._.-._.-._.-._.-._.-._.|
  |_.-._.-._.-._.-._.-._ .::d88b -._.-._ .::d88b -._.-._.-._.-._.-._.-._.|
  |_.-._.-._.-._.-._.-. .::d8888b       .::d8888b ._.-._.-._.-._.-._.-._.|
  |_.-._.-._.-._.-._.- .::d88!::::::::::::d888888b _.-._.-._.-._.-._.-._.|
  |_.-._.-._.-._.-._.- \  Y88\_________\  Y888888P _.-._.-._.-._.-._.-._.|
  |_.-._.-._.-._.-._.-. \  Y8888P ._.-. \  Y8888P ._.-._.-._.-._.-._.-._.|
  |_.-._.-._.-._.-._.-._ /dbY88Pdb _.-._ /dbY88Pdb _.-._.-._.-._.-._.-._.|
  |_.-._.-._.-._.-._.-. /d8P_YP Y8b .-. /d8P_YP Y8b .-._.-._.-._.-._.-._.|
  |_.-._.-._.-._.-     /d8P .-.\ Y8b   /d8P .- \ Y8b -._.-._.-._.-._.-._.|
  |_.-._.-._.-._ .::db/d8P _.-. \.::db/d8P _.-. \ Y8b ._.-._.-._.-._.-._.|
  |_.-._.-._.-. .::d88bYP ._.-. .::d88LSP ._.-._ \ Y8b    ._.-._.-._.-._.|
  |_.-._.-._.- .::d8888b       .::d8888b`b _.-._. \ Y8b:db _.-._.-._.-._.|
  |_.-._.-._. .::d88!::::::::::::d888888b`b .-._.- \ YPd88b .-._.-._.-._.|
  |_.-._.-._. \  Y88\_________\  Y888888Pd8b       .::d8888b -._.-._.-._.|
  |_.-._.-._.- \  Y8888P -._.- \  Y8888P!::::::::::::d888888b ._.-._.-._.|
  |_.-._.-._.-. \  Y88Pdb ._.-. \  Y88Pdb_________\  Y888888P ._.-._.-._.|
  |_.-._.-._.-._ \__YP Y8b _.-._ \__YP Y8b`P -._.- \  Y8888P -._.-._.-._.|
  |_.-._.-._.-._.-._. \ Y8b .-._.-. /d\ Y8b .-._.-. /dbY88P .-._.-._.-._.|
  |_.-._.-._.-._.-._.- \ Y8b -._.- /d8P\ Y8b -._.- /d8P_YP _.-._.-._.-._.|
  |_.-._.-._.-._.-._.-. \ Y8b     /d8P _\ Y8b     /d8P _.-._.-._.-._.-._.|
  |_.-._.-._.-._.-._.-._ \ Y8b:db/d8P ._ \ Y8b:db/d8P ._.-._.-._.-._.-._.|
  |_.-._.-._.-._.-._.-._. \ YPd88bYP -._. \ YPd88bYP -._.-._.-._.-._.-._.|
  |_.-._.-._.-._.-._.-._. .::d8888b       .::d8888b .-._.-._.-._.-._.-._.|
  |_.-._.-._.-._.-._.-._ .::d88!::::::::::::d888888b -._.-._.-._.-._.-._.|
  |_.-._.-._.-._.-._.-._ \  Y88\_________\  Y888888P -._.-._.-._.-._.-._.|
  |_.-._.-._.-._.-._.-._. \  Y8888P .-._. \  Y8888P .-._.-._.-._.-._.-._.|
  |_.-._.-._.-._.-._.-._.- \  Y88P _.-._.- \  Y88P _.-._.-._.-._.-._.-._.|
  |_.-._.-._.-._.-._.-._.-. \__YP ._.-._.-. \__YP ._.-._.-._.-._.-._.-._.|
  `----------------------------------------------------------------------'
                     P Y T H O N   O B F U S C A T O R


    """
    
    colors = ['\033[91m', '\033[92m', '\033[93m', '\033[94m', '\033[95m', '\033[96m']
    
    for line in banner.split('\n'):
        color = random.choice(colors)
        print(color + line + '\033[0m')
        time.sleep(0.05)

def print_status(message, status_type="info"):
    colors = {
        "info": "\033[94m[+]\033[0m",
        "success": "\033[92m[✓]\033[0m", 
        "warning": "\033[93m[!]\033[0m",
        "error": "\033[91m[×]\033[0m",
        "process": "\033[95m[→]\033[0m"
    }
    
    timestamp = time.strftime("%H:%M:%S")
    color = colors.get(status_type, "\033[94m[+]\033[0m")
    print(f"\033[90m[{timestamp}]\033[0m {color} {message}")

def animate_loading(message, duration=2):
    print_status(message, "process")
    
    symbols = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    end_time = time.time() + duration
    
    while time.time() < end_time:
        for symbol in symbols:
            sys.stdout.write(f"\r\033[90m[{time.strftime('%H:%M:%S')}]\033[0m \033[95m[→]\033[0m {message} {symbol}")
            sys.stdout.flush()
            time.sleep(0.1)
            if time.time() >= end_time:
                break
    
    sys.stdout.write(f"\r\033[90m[{time.strftime('%H:%M:%S')}]\033[0m \033[95m[→]\033[0m {message} \033[92mDONE\033[0m\n")
    sys.stdout.flush()

LOADER_TEMPLATE = '''import base64 as b, marshal as m{decompress_import};a={b64!s};b=b.b64decode(a){maybe_decompress};c=m.loads(b);exec(c)'''

def obfuscate_file(input_path: Path, output_path: Path, compress: bool = False):
    print_status(f"Reading source file: {input_path}", "info")
    
    animate_loading("Reading source code", 1)
    src = input_path.read_text(encoding="utf-8")
    
    animate_loading("Compiling to bytecode", 1.5)
    code_obj = compile(src, str(input_path), "exec")
    
    animate_loading("Marshaling code object", 1)
    data = marshal.dumps(code_obj)
    
    if compress:
        animate_loading("Compressing with zlib", 1)
        data = zlib.compress(data)
        print_status("Compression applied: Size reduced", "success")
    
    animate_loading("Encoding with base64", 1)
    b64 = base64.b64encode(data).decode("ascii")
    
    animate_loading("Creating obfuscated loader", 1)
    loader = LOADER_TEMPLATE.format(
        b64=repr(b64),
        decompress_import=";import zlib as z" if compress else "",
        maybe_decompress=";b=z.decompress(b)" if compress else ""
    )
    
    output_path.write_text(loader, encoding="utf-8")
    
    print_status(f"Original size: {len(src)} bytes", "info")
    print_status(f"Obfuscated size: {len(loader)} bytes", "info")
    print_status(f"Output file: {output_path}", "success")
    
    print("\n" + "─" * 60)
    print_status("Obfuscated code preview:", "info")
    print("\033[90m" + "-" * 40 + "\033[0m")
    
    lines = loader.split('\n')
    for i, line in enumerate(lines[:3]):
        print(f"\033[96m{line[:80]}{'...' if len(line) > 80 else ''}\033[0m")
    
    if len(lines) > 3:
        print("\033[90m... [truncated] ...\033[0m")
    
    print("\033[90m" + "-" * 40 + "\033[0m")

def main():
    print_banner()
    
    p = argparse.ArgumentParser(
        description="\033[96mBOMBER OBFUSCATOR\033[0m - Advanced Python code obfuscator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
\033[93mExamples:\033[0m
  python obfuscator.py script.py                    # Basic obfuscation
  python obfuscator.py script.py --compress         # With compression
  python obfuscator.py script.py -o hidden.py       # Custom output name
  python obfuscator.py script.py -o hidden.py --compress
  --compress /Reducing the file size (≈%40-50 decrease)
  
\033[93mFeatures:\033[0m
  • Marshal + Base64 obfuscation
  • Optional zlib compression
  • Preserves original functionality
  • Compatible with Python 3.6+
        """
    )
    
    p.add_argument("input", help="\033[92mInput .py file to obfuscate\033[0m")
    p.add_argument("-o", "--output", help="\033[92mOutput .py file (default: obfuscated_<input>)\033[0m")
    p.add_argument("--compress", action="store_true", help="\033[92mApply zlib compression (recommended)\033[0m")
    
    args = p.parse_args()
    
    inp = Path(args.input)
    if not inp.exists():
        print_status(f"Input file not found: {inp}", "error")
        sys.exit(1)
    
    if inp.suffix != '.py':
        print_status(f"File must have .py extension: {inp}", "warning")
        confirm = input("\033[93mContinue anyway? (y/n): \033[0m").lower()
        if confirm != 'y':
            print_status("Operation cancelled", "info")
            sys.exit(0)
    
    if args.output:
        out = Path(args.output)
    else:
        out = inp.with_name(f"bomber_{inp.name}")
    
    if out.exists():
        print_status(f"Output file exists: {out}", "warning")
        confirm = input("\033[93mOverwrite? (y/n): \033[0m").lower()
        if confirm != 'y':
            print_status("Operation cancelled", "info")
            sys.exit(0)
    
    print_status(f"Starting obfuscation process...", "info")
    print_status(f"Input:  {inp}", "info")
    print_status(f"Output: {out}", "info")
    print_status(f"Compression: {'ENABLED' if args.compress else 'DISABLED'}", "info")
    
    print("\n" + "═" * 60)
    
    try:
        obfuscate_file(inp, out, compress=args.compress)
        
        print("\n" + "═" * 60)
        print_status("Obfuscation completed successfully!", "success")
        
        print("\n\033[93m[!] USAGE INSTRUCTIONS:\033[0m")
        print(f"  Run the obfuscated file: \033[96mpython {out}\033[0m")
        print(f"  File is fully functional and preserves all features")
        
        if args.compress:
            print(f"  \033[92m✓ Compression enabled - Smaller file size\033[0m")
        
    except Exception as e:
        print_status(f"Error during obfuscation: {e}", "error")
        sys.exit(1)
    
    print("\n" + "═" * 60)
    print_status("OBFUSCATOR - Process completed", "info")
    print_status("Remember: With great power comes great responsibility!", "warning")

if __name__ == "__main__":
    main()