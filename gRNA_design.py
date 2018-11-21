import argparse
import re
import sys
import itertools
import numpy as np
import pandas as pd

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

#find segments with right frequency
def filter_fre(fre,multitarget,t):
    sort_index = np.argsort(fre)
    fre.sort()
    if multitarget:#find most abondant segments for CRISPR imaging
        sort=np.flip(sort_index)
        sort=sort[10*t:len(sort)]
        try:
            idx=sort[0:10]
        except:
            idx=sort
        return idx
    else:#find unique segments for CRISPR editing
        i=0
        for j in range(len(fre)):
            if fre[j] ==1:
                i+=1
            else:
                break
        if i != 0:
            return sort_index[0:i]
        else:
            sys.exit('No unique segment found in the input sequence. Please try another sequence!')

#find sequence with PAM
def withpam(seg,idx,pam,ppam):
    gRNA=[]
    pam_arry=[]
    for s in np.array(seg)[idx]:
        if ppam=='3':
            s=s[::-1]
        p = re.findall(pam,s[0:len(pam)])
        if p == s[0:len(pam)]:
            gRNA.append(s[len(pam):length])
            pam_arry.append(p)
    return np.column_stack([pam_arry,gRNA])


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

    parser.add_argument('-dbg',
                        '--debug',
                        default=False,
                        action='store_true',
                        help='debug mode')

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

    #find frequency of segments
    (seg, fre)=frequency(seq,length)

    if debug:
        print('segments:{}'.format(seg))
        print('frequency:{}'.format(fre))

    #iterate through the segments until find gRNA(s)
    i=0
    while len(seg)-i*10>=0:
        idx=filter_fre(fre,multitarget,i)
        if debug:
            print('idx of segments:{}'.format(idx))
        gRNA=withpam(seg,idx,pam,ppam)
        i+=1
        if gRNA.size > 0:
            break

    if gRNA.size == 0:
        sys.exit('No gRNA found. Please try another seqence!')

    if debug:
        print('gRNAs:{}'.format(gRNA))

    #output
    try:
        printing
        print('gRNAs:')
        print(gRNA)
    except:
        print(gRNA)
        pd.DataFrame(gRNA).to_csv(path_or_buf='gRNA.csv')
        print('gRNA sequence saved!')

#This is the start of the program
if __name__=='__main__':
    main()
