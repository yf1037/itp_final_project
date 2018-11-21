import argparse
import re
import sys
import itertools

#exception handling
def seq_check(seq,Cas):
    if re.findall('[agctAGCT]',seq)==list(seq) and (Cas == '9' or '12a'):
        return True
    elif re.findall('[agcuAGCU]',seq)==list(seq) and Cas == '13a':
        return True
    return False

#find frequency of segments
def frequency(seq, length):
    seg=[]
    #find all the segments of length in seq
    for i in range(length):
        seg.append(re.findall('\D{}{}{}'.format('{',length,'}'),seq[i:len(seq)]))
    seg=list(itertools.chain(*seg))#flatten
    seg=list(set(seg))#remove duplicate
    fre=[]
    for s in seg:
        fre.append(len(re.findall(s,seq)))
    return seg, fre

#find unique segments for CRISPR editing
def editing(fre):
    pass

#find most abondant segments for CRISPR imaging
def imaging(fre):
    pass

#find sequence with PAM
def withpam(seg,idx,pam,ppam):
    pass


def main():
    #command line interface
    parser = argparse.ArgumentParser(description='gRNA design tool for CRISPR/Cas')

    parser.add_argument('seq',
                        type = str,
                        help='Input fasta file containing one nucleic acid sequence or a nucleic acid sequence')

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

    parser.add_argument('-p',
                        '--printing',
                        action='store_true',
                        help='Print gRNA seqence')

    #command line processing
    args = parser.parse_args()
    file=args.seq
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

    #try open fasta file, if not, treat input as nucleic acid sequence to analyze
    try:
        seq=''
        with open(file,'r') as f:
            for line in f:
                if not line.startswith('>'):
                    seq+=line.strip()
    except:
        seq=file

    #exceptional handling
    if not seq_check(seq,Cas):
        sys.exit('Please input a nucleic acid sequence!')
    elif len(seq) < length:
        sys.exit('Please input a longer sequence!')
    else:
        print('Computing gRNA...')

    #find frequency of segents
    (seg, fre)=frequency(seq,length)

    #find gRNA in the segments
    if multitarget:
        idx=imaging(fre)
    else:
        idx=editing(fre)
    gRNA=withpam(seg,idx,pam,ppam)

    try:
        printing
        print('gRNAs:')
        print(gRNA)
    except:
        #gRNA.to_csv(path_or_buf='gRNA.csv')
        print('gRNA sequence saved!')

#This is the start of the program
if __name__=='__main__':
    main()
