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
    parser.add_argument('--style',
                        metavar='S',
                        type=str,
                        help='the style template to use in LaTeX')
    parser.add_argument('--alphabet',
                        metavar='A',
                        type=str,
                        help='the alphabet to use to sort entries')
    args = parser.parse_args()

    try:
        stylelist, alphabet = None, None
        if args.style:
            stylelist = tbToTex.user_input_style(args.style)
        if args.alphabet:
            alphabet = tbToTex.user_alphabet(args.alphabet)
        tbToTex.main(args.tbfile, stylelist, alphabet)
        subprocess.call('xelatex main.tex', shell=True)
        print("Success!")
    except Exception as e:
        print('Failed to convert to LaTex')
        print(e)
