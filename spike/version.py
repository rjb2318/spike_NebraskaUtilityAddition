
# This file is generated automatically by dev_setup.py 
# Do not edit
ProgramName = 'SPIKE'
VersionName = 'Development version'
version = '0.99.27'
revision = '518'
rev_date = '27-07-2021'

def report():
    "prints version name when SPIKE starts"
    return '''
    ========================
          {0}
    ========================
    Version     : {1}
    Date        : {2}
    Revision Id : {3}
    ========================'''.format(ProgramName, version, rev_date, revision)
print(report())
