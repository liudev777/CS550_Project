class Access:
  def __init__(self):
    self.accessDict = {}

  def __repr__(self):
    res = ""
    for k, v in self.accessDict.items():
      res += f"\n    <{k}: {v}>"
    return res

  def updateAccessCount(self, client_id):
    self.accessDict[client_id] = self.accessDict.get(client_id, 0) + 1