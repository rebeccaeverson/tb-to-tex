import argparse
import subprocess
import tbToTex

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Translate a TB file into a LaTeX dictionary')
    parser.add_argument('tbfile',
                        metavar='F',
                        type=str,
                        help='the Toolbox file to process')
    args = parser.parse_args()

    try:
        tbToTex.main(args.tbfile)
        subprocess.call('xelatex main.tex', shell=True)
        print("Success!")
    except Exception as e:
        print('Failed to convert to LaTex')
        print(e)
