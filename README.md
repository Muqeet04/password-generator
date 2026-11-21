# Password generator

A small C++ console project that generates a password or prints previously saved entries.

This is an educational example. It uses `rand()` seeded with the current time and stores output in plaintext; use a dedicated password manager for real account credentials.

## Build and run

Use a C++11-compatible compiler, such as GCC:

```sh
g++ -std=c++11 -Wall -Wextra main.cpp -o password-generator
./password-generator
```

On Windows, compile the same source with a C++ compiler and run the resulting executable. Rebuild from `main.cpp` to include source changes; the existing checked-in executable is not rebuilt automatically.

Choose `n` to generate a password, then enter a length from **1 to 4096**. Uppercase `N` also works. The character pool contains uppercase letters, lowercase letters, digits, and punctuation. Individual character categories are not guaranteed to appear in every result.

Each generated password is appended to `pass.txt` in the **current working directory**. Choose `p` (or `P`) to print entries from that file. Do not commit real passwords or share the file.

## Regression checks

With Python 3 and GCC installed, run from the repository root:

```sh
python3 -m unittest discover -s tests -v
```

The checks compile the source and exercise character bounds, requested lengths, invalid input, appending history, and reading saved entries. All generated test data stays in temporary directories. Set `CXX` to select another compatible compiler.

