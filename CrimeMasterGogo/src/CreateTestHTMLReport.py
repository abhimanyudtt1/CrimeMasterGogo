import sys
import ast



def table1(k,v,line) :
        if 'http' in str(v) :
            line = line + "<tr>\
                <td>%s</td>\
                    <td><a href='%s'>link</a></td>\
                </tr>     " % (k, v)
        elif 'passed' == str(v).lower() :
            line = line + "<tr>\
                <td>%s</td>\
            <td bgcolor=lightgreen>%s</td>\
            </tr>     " % (k, v)
        elif 'failed' == str(v).lower() :
            line = line + "<tr>\
                <td>%s</td>\
                <td bgcolor=red>%s</td>\
            </tr>     " % (k, v)
        else :
            line = line + "<tr>\
                <td>%s</td>\
                <td>%s</td>\
            </tr>     " % (k, v)
        return line

def createTestReport(report, FH):
    passed = 0
    failed = 0
    msg = '''<h1>Test Summary</h1>
            <br><br>
            <h2>Test Status</h2>
                    '''
    for i in report.values():
        if i[1] == 'Passed':
            passed += 1
        else:
            failed += 1
    if not failed :
        msg += '''<h3 style= "color : Green">Passed</h3><br><br>
                '''
    else :
        msg += '''<h3 style= "color : Red">Failed</h3><br><br>
                '''


    table = "<table border='1'>"
    table = table1('Time taken sec(s)  ', sys.argv[6], table)
    table = table1('Environment', sys.argv[2], table)
    table = table1('Final End Point', sys.argv[4], table)
    table = table1('Date', sys.argv[3], table)
    table = table1('Log URL', sys.argv[5], table)
    table = table1('Total Test Cases', passed + failed, table)
    table = table1('Tests Failed', failed, table)
    table = table1('Tests Passed', passed, table)
    table = table1('Tests Noticed', 'TBD', table)
    table = table1('%age Passed', passed * 100.0 / (passed + failed), table)
    table = table + "</table>"
    msg += table+"<br><br><br>"
    table = "<table border='1'>"
    for i in report.values():
        table = table1(i[0],i[1],table)
    msg += table
    open('./report.html','w').write(msg)






if __name__ == '__main__':
    report = sys.argv[1]
    report = open('%s' % report,'r')
    for line in report :
        report = ast.literal_eval(line)
        break
    import collections

    FH = sys.argv[2]
    createTestReport(collections.OrderedDict(sorted(report.items())),FH)
