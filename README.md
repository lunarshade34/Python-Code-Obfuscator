# Python-Code-Obfuscator

Python Obfuscator (Marshal + Base64 + Optional Zlib)
Overview

This project is an advanced Python source code obfuscator designed to make Python scripts harder to read and reverse-engineer.
It converts readable Python source code into bytecode, then protects it using marshal serialization, Base64 encoding, and optional zlib compression.

This is not encryption. It is code obfuscation intended for intellectual property protection and educational purposes.

Features

Bytecode Obfuscation

Compiles Python source into bytecode using compile()

Serializes the bytecode with marshal to remove readable source code

Base64 Encoding

Encodes marshaled bytecode so it can be safely embedded inside a Python loader

Optional Zlib Compression

Reduces file size by approximately 40–50%

Adds an extra layer of complexity to the output

Fully Functional Output

The obfuscated file runs exactly like the original

No functionality is removed or altered

Animated CLI Interface

Colorful banner

Status messages

Loading animations

Compatibility

Works with Python 3.6 and newer versions

How It Works (Technical Summary)

Reads the original .py file

Compiles the source code into a Python code object

Serializes the code object using marshal

Optionally compresses the serialized data using zlib

Encodes the result using Base64

Generates a minimal loader script that:

Decodes the Base64 data

Decompresses it (if enabled)

Loads and executes the bytecode at runtime

Usage

Basic usage:

python obfuscator.py script.py


With compression:

python obfuscator.py script.py --compress


Custom output file:

python obfuscator.py script.py -o hidden.py

Output

Default output filename:

<original_filename>.py


The generated file:

Contains no readable source code

Executes normally using:

python output.py

Important Notes

This tool does not provide cryptographic security

Obfuscated code can still be deobfuscated by experienced reverse engineers

It is designed to:

Protect scripts from casual copying

Hide logic from beginners

Demonstrate Python internals such as bytecode and marshal serialization

Legal and Ethical Disclaimer

This project is intended for educational purposes and intellectual property protection only.

Do NOT use this tool to:

Hide malware

Evade security systems

Bypass licenses or DRM

Distribute malicious code

You are solely responsible for how you use this software.

Educational Value

This project demonstrates:

Python bytecode internals

Marshal serialization

Runtime execution techniques

Code obfuscation concepts

Command-line interface user experience improvements in Python
