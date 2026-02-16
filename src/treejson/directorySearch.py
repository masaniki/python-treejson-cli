import sys
from pathlib import Path
import argparse
import yaml
import json

VERSION="v1.1.0"

def main():
    """
    @Summ: CLIを処理する関数。
    """
    parser=argparse.ArgumentParser(prog="treejson")
    parser.add_argument("dirName",type=str,default=None,help="Put in directory name.")
    parser.add_argument("-v","--version",action="version",version="%(prog)s"+f"{VERSION}")
    parser.add_argument("-y","--yaml",action="store_true",help="Output as a YAML format.")
    parser.add_argument("-a","--all",action="store_true",help="Visit hidden file.")
    parser.add_argument("-f","--file",type=str,help="Output as a file.")
    parser.add_argument("-m","--max",type=int,help="Specify maximum depth.")
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
