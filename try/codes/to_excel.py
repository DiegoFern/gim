import pandas as pd
import sys
print(sys.argv)
w = pd.ExcelWriter(sys.argv[2],engine='xlsxwriter')
pd.read_csv(sys.argv[1]).to_excel(w)
w.save()
