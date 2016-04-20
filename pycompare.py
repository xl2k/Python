#!/usr/local/bin/python2.7
# encoding: utf-8
'''
pycompare -- python script to compare 2 csv files


pycompare is a description

complete the exludes swtich 2014-05-25

@author:     user_name
        
@copyright:  2014 organization_name. All rights reserved.
        
@license:    license

@contact:    user_email
@deffield    updated: 2014-05-15
'''

import sys
import os
import csv
 

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

__all__ = []
__version__ = 0.8
__date__ = '2014-02-06'
__updated__ = '2014-07-23'
__todo__ = 'switch to check extended ascii in source or dest file'

DEBUG = 0
TESTRUN = 0
PROFILE = 0

DIALECT = 'excel'
HEADER_BUFFER_SIZE = 4096 # if header is very big, this number needs to be increased

CASE_CENSITIVE = True  # this can be overwritten with optional switch


def upcase(s):
    return s.upper();
def quote(s):
    return '"' + s + '"'

def replace(s, repl_lst): # here repl_lst is the ascii code list

    def swap(a,l):
        if a in l:
            return 32
        else:
            return a

    ll = [chr(swap(ord(x),repl_lst)) for x in s]
    #print ll
    return ''.join(ll)

    
def exclude(lst, excludes): #excludes is column index[String] in list. 
    dct = {}
    for i in xrange(0,len(lst)): dct[i] = lst[i]
    d = {i:dct[i] for i in dct if str(i) not in excludes}
    nlst = d.values()
    return nlst

class View(object):
    ''' this is the view to display the result
    '''
    def __init__(self, data):
        self.data = data
        
    def display(self):
        for item in self.data:
            print ",".join(map(quote,item))
    

class Comparer(object):
    
    @staticmethod
    def loadData(fname, caseSensitive):
        lst = []
        with open(fname,'rb') as csvfile:
            reader = csv.reader(csvfile,  dialect=DIALECT)
            for row in reader:
                lst.append(tuple(row)) # convert list to tuple for each row
        return lst


        
    def __init__(self, source, dest, caseSensitive = True, excludes = None, columns = None, repl = None):
        
        self.source = source
        self.dest = dest
        
        self.source_header = []
        self.dest_header = []
        self.source_list = []
        self.dest_list = []
        self.caseSensitive = caseSensitive
        self.excludes = excludes
        self.columns = columns
        self.replaces = repl
        
        whole_csv_lst = self.loadData(self.source, self.caseSensitive)
        if self.hasHeader():
            self.source_header = whole_csv_lst[0]
            self.source_list = whole_csv_lst[1:] # get rid of the header
        else:
            self.source_list = whole_csv_lst 

        whole_csv_lst = self.loadData(self.dest, self.caseSensitive)
        if self.hasHeader():
            self.dest_header = whole_csv_lst[0]
            self.dest_list = whole_csv_lst[1:] # get rid of the header
        else:
            self.dest_list = whole_csv_lst 
        
        
    def __str__(self):
        return self.msg

    def setCaseSensitive(self, caseSensitive):
        self.caseSensitive = caseSensitive
        
    def setExcludes(self, indexes): # set excluded indexes of column, they won't get compared
        self.excludes = indexes
    
    def setColumns(self, indexes):
        self.columns = indexes # set compared indexes of columns, only compare the columns

    def setReplaces(self, replaces): # replaces is a list of ascii code
        self.replaces = replaces 
        
    

    def dumpSource(self):
        print self.source_list

    def dumpDest(self):
        print self.dest_list
            
    def hasHeader(self):
        return self.hasSourceHeader() or self.hasDestHeader()
        
    def hasSourceHeader(self):
        with open(self.source,'rb') as csvfile:
            return csv.Sniffer().has_header(csvfile.read(HEADER_BUFFER_SIZE))
    
    def hasDestHeader(self):
        with open(self.dest,'rb') as csvfile:
            return csv.Sniffer().has_header(csvfile.read(HEADER_BUFFER_SIZE))
        
    def getSourceHeader(self):
        return self.source_header
    
    def getDestHeader(self):
        return self.dest_header
    
    def compareHeader(self):
         
        def isSameHeader(t):         # nested function defined, not being called yet
            if self.caseSensitive:
                return t[0] == t[1]
            else:
                return t[0].upper() == t[1].upper()
        
        boolean_matrix = map(isSameHeader,zip(self.getSourceHeader(), self.getDestHeader()))
        # [True, True, False ...]
        print self.getSourceHeader()
        print self.getDestHeader()
        
        if False in boolean_matrix:
            print "Header differences..."
            for x in zip(boolean_matrix, range(len(boolean_matrix)), self.getSourceHeader(), self.getDestHeader()):
                if not x[0]:
                    print x[1] # index of the column 
                    print x[2] # source heading
                    print x[3] # dest heading
                
    def rowcount(self):
        print "source file row count and destination file row count difference:"
        print len(self.source_list) - len(self.dest_list)
    
    def compareBody(self):
        lstSrc = []
        lstDst = []
        
        for row in self.source_list:

            # here is a hack
            unicode_list = list(row)
            lst_src_row = []
            for u in unicode_list:
                x=u.decode('ascii','ignore').strip()
                lst_src_row.append(x)
           

            if self.excludes:
                lst_src_row = exclude(lst_src_row, self.excludes)
            
            if self.columns:
                lst_src_row = [lst_src_row[int(self.columns[0])].strip()]  # todo: only works with 1 column for now

            if self.replaces:
                lst_src_row = [replace(item, self.replaces) for item in lst_src_row]

            
            if not self.caseSensitive:
                lstSrc.append(tuple(map(upcase,lst_src_row)))
            else:
                lstSrc.append(tuple(lst_src_row))

            
                
        for row in self.dest_list:

            # here is a hack
            unicode_list = list(row)
            lst_dst_row = []
            for u in unicode_list:
                x=u.decode('ascii','ignore').strip()
                lst_dst_row.append(x)
            
            if self.excludes:
                lst_dst_row = exclude(lst_dst_row, self.excludes)

            if self.columns:
                lst_dst_row = [lst_dst_row[int(self.columns[0])].strip()]  # todo: only works with 1 column for now
                

            if self.replaces:
                lst_dst_row = [replace(item, self.replaces) for item in lst_dst_row]
          
            
            if not self.caseSensitive:
                lstDst.append(tuple(map(upcase,lst_dst_row)))
            else:
                lstDst.append(tuple(lst_dst_row))
                
        
        diff_source_minutes_dest = set(lstSrc) - set(lstDst)
        print "records in source file but not in destination file:", len(diff_source_minutes_dest)
        
        View(diff_source_minutes_dest).display()
        
        
        diff_dest_minutes_source = set(lstDst) - set(lstSrc)
        print "records in destination file but not in source file:", len(diff_dest_minutes_source)
        
        View(diff_dest_minutes_source).display()
        

class CLIError(Exception):
    '''Generic exception to raise and log different fatal errors.'''
    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg
    def __str__(self):
        return self.msg
    def __unicode__(self):
        return self.msg

def main(argv=None): # IGNORE:C0111
    '''Command line options.'''
    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    program_version = "v%s" % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (program_version, program_build_date)
    program_shortdesc = __import__('__main__').__doc__.split("\n")[1]
    program_license = '''%s

  Created by user_name on %s.
  Copyright 2014 organization_name. All rights reserved.
  
  Licensed under the Apache License 2.0
  http://www.apache.org/licenses/LICENSE-2.0
  
  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
''' % (program_shortdesc, str(__date__))

    try:
        # Setup argument parser
        #parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)
        parser = ArgumentParser()
        parser.add_argument("-V", "--version", action="version", version=program_version_message)
        parser.add_argument("-I", "--Info",action="store_true", help="displays overall csv files info")
        parser.add_argument("-i", "--caseInsensitive", action="store_true", help="case insensitive in compare")
        parser.add_argument("-x", "--excludes",action="store", help="excluded column(s)")
        parser.add_argument("-c", "--columns",action="store", help="specify compared column(s)")
        parser.add_argument("-p", "--replaces",action="store", help="replacing special characters")
        parser.add_argument(dest="source_csv_file", help="path to folder(s) with source csv file(s) [default: %(default)s]")
        parser.add_argument(dest="dest_csv_file", help="path to folder(s) with dest csv file(s) [default: %(default)s]")
        
        # Process arguments
        
        args = parser.parse_args()
        
        source = args.source_csv_file
        dest = args.dest_csv_file
        
        
        CASE_CENSITIVE = not args.caseInsensitive
       
        comp = Comparer(source, dest, CASE_CENSITIVE)
        
        if args.Info:
            print "Has header:", comp.hasHeader()
            return 0
        
        #comp.setCaseSensitive(CASE_CENSITIVE)
        
        if args.excludes: # set the column indexes which excluded from comparing
            comp.setExcludes(args.excludes.split(","))
            # todo: -x and -c mutual exclusive how to enforce that

        if args.replaces:
            l= args.replaces.split(",")
            comp.setReplaces(l)
        
        if args.columns:
            comp.setColumns(args.columns.split(","))
            
        
        comp.compareHeader()
        comp.compareBody()
        
        
        return 0
    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0
    except Exception, e:
        if DEBUG or TESTRUN:
            raise(e)
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2

if __name__ == "__main__":
    if DEBUG:
        sys.argv.append("-h")
        sys.argv.append("-v")
        sys.argv.append("-r")
    if TESTRUN:
        import doctest
        doctest.testmod()
    if PROFILE:
        import cProfile
        import pstats
        profile_filename = 'pycompare_profile.txt'
        cProfile.run('main()', profile_filename)
        statsfile = open("profile_stats.txt", "wb")
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)
    
    sys.exit(main())
