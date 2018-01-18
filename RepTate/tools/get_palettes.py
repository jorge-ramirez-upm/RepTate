import seaborn as sns
# Palette names = pastel, bright, 
NCOLORS=16
PALETTE="Paired"
p = sns.color_palette(PALETTE,NCOLORS)
newp=[]
for i in range(len(p)):
    x=(round(p[i][0],3), round(p[i][1],3), round(p[i][2],3))
    newp.append(x)
print(newp)