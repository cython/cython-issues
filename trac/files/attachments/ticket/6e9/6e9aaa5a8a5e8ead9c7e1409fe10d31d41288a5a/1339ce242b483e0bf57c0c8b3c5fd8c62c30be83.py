def Update(self, end_time):
     
     
     while self._fIndex < len(self.fLogicalList):
         logical = None 
         
         if logical.fIndentLevel == 0: # or prior is None:
             logical.SetScopeName('')
             del self._fActiveScopeDefs[:]
             

     return False

def test():
     class S:
          pass
     s = S()
     s._fIndex = 0
     s.fLogicalList = []
     Update(s, 0)
     