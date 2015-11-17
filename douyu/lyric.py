import re

class Lyric():
    def __init__(self, down_lyric):
        self.lyric_lines=down_lyric.split('\n')
        self.pattern=re.compile(r'\[(.+):(.+)\.(.+)\](.*)')
        self.time_minus=[]
        self.cut_lyric=[]

    def get_line_lyric(self,line):
        m = self.pattern.match(line)
        if m!=None:
            return m.group(1),m.group(2),m.group(3),m.group(4)
        else:
            return None

    def process_lyric(self):
        for v in self.lyric_lines:
            try:
                if self.get_line_lyric(v)!=None:
                    mnt,sec,mili,content=self.get_line_lyric(v)
                    if len(mili)==3:
                        #print(int(mnt)*60+int(sec)+int(mili)/1000)
                        self.time_minus.append(int(mnt)*60+int(sec)+int(mili)/1000)
                    elif len(mili)==2:
                        self.time_minus.append(int(mnt)*60+int(sec)+int(mili)/1000)
                    self.cut_lyric.append(content)
                else:
                    print('无歌词1')
            except Exception as e:
                print('无歌词2')
        #print(self.cut_lyric)
        # print(len(self.cut_lyric))
        for i,v in enumerate(self.time_minus):
            if i<len(self.time_minus)-1:
                self.time_minus[i]=round(self.time_minus[i+1]-self.time_minus[i],3)
        #print(self.time_minus)
        # print(len(self.time_minus))
        try:
            firstm,firstsec,firstmili,firstcontent=self.get_line_lyric(self.lyric_lines[0])
            if firstm=='00' and firstsec=='00' and (firstmili=='00' or firstmili=='000'):
                pass
            else:
                self.cut_lyric.insert(0,'')
                if len(mili)==3:
                    self.time_minus.insert(0,int(firstm)*60+int(firstsec)+int(firstmili)/1000)
                elif len(mili)==2:
                    self.time_minus.insert(0,int(firstm)*60+int(firstsec)+int(firstmili)/100)
                else:
                    print('lyric error')
            #print('########################')
            #print(self.time_minus)
        except Exception as e:
            print('无歌词3')