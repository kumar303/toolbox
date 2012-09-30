#!/usr/bin/env python

import PalmDB

pdb = PalmDB.File('/Users/kumar/tmp/BB4-Transactions.pdb')
for r in pdb.getRecords():
    print r.id, r.raw