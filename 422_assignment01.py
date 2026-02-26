# task1
n, m = map(int, input("maze height and width: ").split())
st_R,st_C = map(int, input("start (r c): ").split())
gRow,gCol = map(int, input("goal (r c): ").split())
print(f" {n} rows of the maze:")
maze=[]
for lang in range(n):
    row =input()
    mazerow = []

    for ch in row:
      mazerow.append(ch)
    maze.append(mazerow)

step = [(1, 0, 'D'), (0, -1, 'L'), (-1, 0, 'U'),(0, 1, 'R')]

def Gdist(r, c):
  rowD=r-gRow
  if rowD < 0:
    rowD=-rowD

  colD = c - gCol
  if colD < 0:
    colD = -colD

  return rowD + colD

def a_st_fun():
  verify = []
  for i in range(n):

    verify.append([False]*m)


  path_togo = []
  h = Gdist(st_R, st_C)
  path_togo.append([h, 0, st_R, st_C, ""])

  while path_togo:
    path_togo.sort()
    fcost, g,x,y,path=path_togo.pop(0)


    if (x, y)==(gRow, gCol):
      print(f"{g}")
      print(f"{path}")
      return

    if verify[x][y]:
      continue
    verify[x][y]=True

    for step_x,step_y, d in step:
      newR=x +step_x
      newC =y +step_y
      if 0 <= newR <n and 0 <=newC < m:
        if maze[newR][newC]=='0' and not verify[newR][newC]:
          cost=g+1
          tot_cost= cost+ Gdist(newR, newC)
          path_togo.append([tot_cost, cost, newR, newC, path + d])
  print(-1) 
a_st_fun()

# task2#########################################################################3

inp= """ 6 7 
 
1 6 
 
1 6 
2 4 
3 2 
4 5 
5 2 
6 0 
 
1 2 
2 3 
3 6 
1 4 
4 5 
5 6 
3 5"""

L = inp.split('\n')  
val_line = []
for i in L:
  i = i.strip()
  if i != '':
    val_line.append(i)

def input():
    return val_line.pop(0)

n, m = map(int, input().split())
st, goal = map(int, input().split())


heu={}
for count in range(n):
  n, val = map(int, input().split())
  heu[n] = val


graph_adj={}
for i in range(1, n+1):
    graph_adj[i] = []  

for i in range(m):
  u, v = input().split()
  u = int(u)
  v = int(v)
  graph_adj[u].append(v)  
  graph_adj[v].append(u) 

lang = []
q = [st]
vis = {st: True}
pos = 0

while pos<len(q):
  now = q[pos]
  pos += 1

  for next in graph_adj[now]:
    if heu[next] > heu[now] +1:
      if next not in lang:

        lang.append(next)
    if heu[now] > heu[next]+1:
      if now not in lang:
        lang.append(now)

    if next not in vis:
      vis[next] = True
      q.append(next)

if len(lang) == 0:
  print("1")


else:
  print("0")
  print("Here the nodes", end=" ")
  for i in range(len(lang)):

    if i==len(lang) - 1:
      print(f"{lang[i]}", end=" ")
    elif i==len(lang)-1 and len(lang)>1:

      print(f"\nand {lang[i]}", end=" ")

    else:
      print(f"{lang[i]}, ", end="")
  print("are inadmissible.")
