import sys
from pathlib import Path
import argparse
import yaml
import json

VERSION="v1.0.2"

def main():
    """
    @Summ: CLIを処理する関数。

    @Returns:
        @Type: dict
        @Summ: {directory名(str):[i(int):i番目の子directory名(str)]}という木構造。
    """
    parser=argparse.ArgumentParser(prog="treejson")
    parser.add_argument("dirName",type=str,default=None,help="put in directory name.")
    parser.add_argument("-v","--version",action="version",version="%(prog)s"+f"{VERSION}")
    parser.add_argument("-y","--yaml",action="store_true",help="output as a YAML format.")
    parser.add_argument("-a","--all",action="store_true",help="visit hidden file.")
    parser.add_argument("-f","--file",type=str,help="output as a file.")
    parser.add_argument("-m","--max",type=int,help="specify maximum depth.")
    parser.add_argument("-d","--default",type=str,help="Specify default scalar.")
    args=parser.parse_args()
    if(args.max<0):
        raise ValueError(f"--max option should be positive integer.")
    dirPath=Path(args.dirName)
    dirSearch=DirectorySearch(maxDepth=args.max,isAll=args.all,default=args.default)
    outDict=dirSearch.traversal(dirPath)
    if(args.yaml):
        if(args.file is None):
            yaml.safe_dump(outDict,sys.stdout,allow_unicode=True)
        else:
            with open(args.file,mode="w",encoding="utf-8") as f:
                yaml.safe_dump(outDict,f,allow_unicode=True)
    else:
        if(args.file is None):
            print(outDict)
        else:
            with open(args.file,mode="w",encoding="utf-8") as f:
                json.dump(outDict,f)

def directoryBFS(startDir:Path,maxDepth:int=None,isAll:bool=None):
    """
    @Summ: directory構造を幅優先探索する関数。

    @Args:
      startDir:
        @Type: Path.
        @Summ: 探索を開始するdirectory名。
      maxDepth:
        @Type: Int.
        @Summ: 探索の最大の深さ。
        @Desc:
        - current directoryは深さ0。
        - 「maxDepth<現在の深さ」の時に探索打ち切り。
        @Default: 255.
      isAll:
        @Type: Bool.
        @Summ: {True⇒隠しfileも探索, False⇒隠しfileを通過。}
        @Default: false.
    @Returns:
      @Type: dict
      @Summ: {directory名(str):[i(int):i番目の子directory名(str)]}という木構造。
      @Desc:
      - {directory名(str):[i(int):i番目の子directory名|file名(str)]}。
      - file名の時は、終端nodeになる。
    """
    if(maxDepth is None):
        maxDepth=255
    if(isAll is None):
        isAll=False
    outDict={startDir.name:[]}
    visitQueue=[startDir]  #訪れるdirectory(Path型)を格納する。
    listQueue=[outDict[startDir.name]]  #訪れるdirectoryの子要素のlist型を格納する。
    depthQueue=[0]  #訪れるdiectoryの深さ(int型)を格納する。
    while(True):
        if(visitQueue==[]):
            break
        curDir=visitQueue.pop(0)
        curList=listQueue.pop(0)
        curDepth=depthQueue.pop(0)
        nextDepth=curDepth+1
        if(maxDepth<nextDepth):
            continue
        for childPath in curDir.iterdir():
            childName=childPath.name
            firstChr=childName[0]
            if((not isAll) and firstChr=='.'):
                continue
            if(childPath.is_file()):
                curList.append(childName)
            else:
                childDict={childName:[]}
                curList.append(childDict)
                visitQueue.append(childPath)
                listQueue.append(childDict[childName])
                depthQueue.append(nextDepth)
    return outDict

class DirectorySearch():
    """
    @Summ: directoryを再帰関数で探索する関数。

    @InsVars:
      depth:
        @Summ: 現在探索している所の深さ。
        @Type: Int
      maxDepth:
        @Summ: 探索する最大の深さ。
        @Desc:
        - current directoryは深さ0。
        - defaultでは10。
        - 「maxDepth<現在の深さ」の時に探索打ち切り。
        @Type: Int
      isAll:
        @Summ: 隠しfileも探索する時にTrue.
        @Desc: defaultではFalse。
        @Type: Bool
      default:
        @Summ: 終端nodeに代入するscalar値。
        @Desc: 代入する値はscalar型ならば何でもよい。
        @SemType: scalar
    """
    def __init__(self,maxDepth=None,isAll=None,default=None):
        if(maxDepth is None):
            maxDepth=10
        if(isAll is None):
            isAll=False
        if(type(default)==dict):
            raise TypeError(f"Default value should be scalar.")
        elif(type(default)==list):
            raise TypeError(f"Default value should be scalar.")
        self.maxDepth=maxDepth
        self.isAll=isAll
        self.default=default
        self.depth=0
    
    def traversal(self,curPath:Path)->dict:
        """
        @Summ: 探索を実行する関数。

        @Desc: fileは探索しない。directoryのみを探索する。

        @Args:
          curPath:
            @Summ: 探索するdirectory.
            @ComeFrom: current path.
            @Type: Path
        @Returns:
          @Summ: 探索結果を記録するdict型かscalar。
          @SemType: Dict|scalar
        """
        # fileの探索。
        if(curPath.is_file()):
            return self.default
        # 深さで枝狩り。
        self.depth+=1
        if(self.maxDepth<self.depth):
           return {}
        # directoryの探索。
        outDict={}
        for childPath in curPath.iterdir():
            if(not self.isAll and childPath.name[0]=="."):
                continue
            childValue=self.traversal(childPath)
            outDict[childPath.name]=childValue
        self.depth-=1
        return outDict


if(__name__=="__main__"):
    main()
