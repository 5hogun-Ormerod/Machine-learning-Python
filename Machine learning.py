

import csv


class DecisionTree():
    
    tree ={}
     
    def learn(self, training_set):
        self.tree = {}
        tol = .90
        res = [self.best_attr_str(data,k) if isinstance(data[0][k],str) else self.best_attr_int(data,k) for k in [x if x < 2 else x+1 for x in range(13)]]
        print(res)
	
	# I am not decided on the data type yet, but the above is the way in which I choose the critera
                
    def best_attr_str(self,rows, column):
        values = list(set([x[column] for x in rows]))
        bestval = values[0]
        maxgini = 0
        if len(values) > 1:
            for val in values:
                (inc,notinc) = divideset(rows,column,val)
                (inctrue,incfalse) = divideset(inc,-1,'>50K')
                p = len(inctrue)/len(inc)
                gini = p*(1-p)
                if p > 1-p:
                    bestval = val
                    maxgini = gini
                    test = True
                else:
                    bestval = val
                    maxgini = gini
                    test = False                
        return [bestval,maxgini,test]
        
    def best_attr_int(self,rows, column):
        values = list(set([x[column] for x in rows]))
        maxval = max(values)
        minval = min(values)
        bestval = minval
        maxgini = 0
        test = True
        for theta in values:
            (inc,notinc) = divideset(rows,column,theta)
            if len(inc) > 10:
                (inctrue,incfalse) = divideset(inc,-1,'>50K')
                p = len(inctrue)/len(inc)
                gini = p*(1-p)
                if gini > maxgini:
                    bestval = theta
                    maxgini = gini
                    if p > 1-p:
                        test = True
                    else:
                        test = False
        return [bestval,maxgini, test]    
                
    def divideset(self,rows,column,value):
        split_function=None
        if isinstance(value,int) or isinstance(value,float):
            split_function=lambda row:row[column]<=value
        else:
            split_function=lambda row:row[column]==value
   
        set1=[row for row in rows if split_function(row)] # if split_function(row) 
        set2=[row for row in rows if not split_function(row)]
        return (set1,set2) 
       
    def classify(self, test_instance):
        result = "<=50K" # baseline: always classifies as <=50K
		
        return result
    def convert(value):
        if isinstance(value,int):
            return value
        else:
            if isinstance(value,str):
                if value.isdigit():
                    return int(value)
                else:
                    return value
            else:
                return value

def run_decision_tree():
    with open("hw4-task1-data.tsv") as tsv:
        data = [tuple(line) for line in csv.reader(tsv, delimiter="\t")]
    data = [list(map(convert,x)) for x in data]
    t = DecisionTree()
    t.learn(data)  



if __name__ == "__main__":
	run_decision_tree()
