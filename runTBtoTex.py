import argparse
import subprocess

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Translate a TB file into a LaTeX dictionary')
    parser.add_argument('tbfile',
                        metavar='F',
                        type=str,
                        help='the Toolbox file to process')
    args = parser.parse_args()

    subprocess.call('python tbToTex.py ' + args.tbfile, shell=True)
    subprocess.call('xelatex main.tex', shell=True)

    print("Success!")
