import argparse
import re
import sys

#exception handling
def seq_check(seq,Cas):
    if re.findall('[agctAGCT]',seq)==list(seq) and (Cas == '9' or '12a'):
        return True
    elif re.findall('[agcuAGCU]',seq)==list(seq) and Cas == '13a':
        return True
    return False

#find unique segments for CRISPR editing


#find most abondant segments for CRISPR imaging


#find segments with PAM


#return gRNA

#command line interface
def main():
    # Create a parser:
    parser = argparse.ArgumentParser(description='gRNA design tool for CRISPR/Cas')

    parser.add_argument('seq',
                        type = str,
                        help='DNA/RNA sequence or fasta file location')

    parser.add_argument('-c',
                        '--Cas',
    					help='The type of CRISPR/Cas system',
                        choices=['9','12a','13a'],
                        default='9')

    parser.add_argument('-l',
                        '--length',
                        type=int,
                        help='Length of gRNAs',
                        default=20)

    parser.add_argument('-u',
                        '--use',
                        choices=['editing','imaging'],
                        default='editing',
                        help='Usage of the gRNA')

    args = parser.parse_args()
    seq=args.seq
    length=args.length
    Cas=args.Cas
    if Cas == '9':
        pam='gg'
        ppam='5'
    elif Cas == '12a':
        pam='ttt[agc]'
        ppam='5'
    else:
        pam='[auc]'
        ppam='3'
    if args.use == 'imaging':
        multitarget= True
    else:
        multitarget= False

    if not seq_check(seq,Cas):
        sys.exit('please input a nucleic acid sequence!')
    else:
        print('so far so good!')

#This is the start of the program
if __name__=='__main__':
    main()
