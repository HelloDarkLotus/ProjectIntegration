import csv


class DataAnalysis(object):
    def __init__(self, csvFile):
        self.file = csvFile
        self.stsTbl = dict()
        self.totalNum = 0

    def GenDataDict(self):
        with open(self.file) as f:
            handler = csv.reader(f)
            next(handler)
            self.totalNum = len(list(handler))
            for row in handler:
                if 'New' in row:
                    self.stsTbl[r'New'] += 1
                elif 'Assigned' in row:
                    self.stsTbl[r'Assigned'] += 1
                elif 'Working' in row:
                    self.stsTbl[r'Working'] += 1
                elif 'Resolved' in row:
                    self.stsTbl[r'Resolved'] += 1
                elif 'Rejected' in row:
                    self.stsTbl[r'Rejected'] += 1
                elif 'Verified' in row:
                    self.stsTbl[r'Verified'] += 1
                elif 'Closed' in row:
                    self.stsTbl[r'Closed'] += 1
                else:
                    self.stsTbl[r'Pending'] += 1