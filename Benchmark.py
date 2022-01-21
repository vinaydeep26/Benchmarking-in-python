import threading
import time
import datetime
import numpy as np
import matplotlib.pyplot as plt

#----------------------------------------------------------------------------------The Threading class
class mythread(threading.Thread):
    _terminate=False                            #FLAG TO STOP LOOP
    list1=[]                                    #A list to store values of operations
    def __init__(self,threadid):          
        self.threadid=threadid+1
    def count(self):                            #COUNT FUNCTION COUNTS THE NUMBER OF LOOP ITERATIONS
        i=0
        print("Thread "+ str(self.threadid) +" starts.\n")
        while not self._terminate:
            i+=1
            #Uncomment next line to run for Floating point operations
            #flop=1.1*2.5
        self.list1.append(i)
        print("the loop for thread "+ str(self.threadid)+" ran for a total of " +str(i)+ " iterations\n")
        
    def Termination(self):
        self._terminate=True                     #Sets Flag to True to come out of loop

    def run(self):
        t1=threading.Thread(target=self.count)                 #creates and starts thread
        t1.start()

 #----------------------------------------------------------------------------------- Main Thread
time1=time.time()
       
loop1=0
loop2=0
loop3=0
timeinsec=0
x=0
for loop3 in range(0,4):                                      #LOOP TO START 1,2,4,8 THREADS
    if loop3==0:
        n=1
        print("STARTING "+str(n)+" THREADS")
    elif loop3==1:
        n=2
        print("STARTING "+str(n)+" THREADS")
    elif loop3==2:
        n=4
        print("STARTING "+str(n)+" THREADS")
    else:
        n=8
        print("STARTING "+str(n)+" THREADS")
    for loop2 in range(3):                                   #this loop is to Run the program for 3 different times ( 1 ,3 and 5 minutes)
        if loop2==0:
            timeinsec=60
            print("starting threads for time: " + str(timeinsec)+ " seconds\n")
        elif loop2==1:
            timeinsec=180
            print("starting threads for time: " + str(timeinsec)+ " seconds\n")
        else:
            timeinsec=300
            print("starting threads for time: " + str(timeinsec)+ " seconds\n")

            
        for loop1 in range(3):                               #This loop is to RUN THE PROGRAM 3 times
            templist=[]                                      
            for i in range(n):                  
                threadTemp=mythread(i)
                templist.append(threadTemp)
            for t in templist:
                t.run()
            time.sleep(timeinsec)
            for m in templist:
                m.Termination()
            loop1+=1
        loop2=loop2+1
    time.sleep(1)
    #print(mythread.list1)    #This has all the value of iterations taking part in the program. it has 9,18,36,72 values at the end of each loops for 1,2,4,8 threads.

    
    #------------------------------------------------------------Calculation part
    
    alist=mythread.list1[0:n*3]                                    
    averagevalues1= [int(number / 60) for number in alist]          #These 3 lists are to store values of iterations. we split them and then divide them by time run to get OPS
    blist=mythread.list1[n*3:2*n*3]
    averagevalues2= [int(number / 180) for number in blist]         
    clist=mythread.list1[2*n*3:3*n*3]                               
    averagevalues3= [int(number / 300) for number in clist]          
    #print(alist,blist,clist)                                       #uncomment to view all iterations of a thread.
    #print(averagevalues1,averagevalues2,averagevalues3)            #uncomment to view average operations per second values.
    avg=averagevalues1+averagevalues2+averagevalues3
    #print (avg)                                                            
    tempav=0
    for item in avg:
        tempav=item + tempav                               
    average=int(tempav/len(avg))
    print("The Average of all iterations is :" + str(average)+ " operations per second\n")
    avgingflops=average/1000000000                                                                     #we take average in Gigaflops
    print("Average in Giga operations per second is " + str(avgingflops)+"\n")
    std = int(np.std(avg))
    print("The standard deviation is "+ str(std)+"\n")                                                 #standard deviation
    time.sleep(1)                                        
    print("exit main thread\n")
    loop3+=1

'''
the 3 lists alist b list and clist split the values in equal parts, so for 1 thread we have n=1 so 3 values each for 3 different times
for n=2 it splits by 6 6 6 and for n=4 it does 12 12 12.
for example if we have vlaues for 1 thread running 3 times for 2 seconds then 4 then 6 seconds
example values are 1200 1200 1200 2400 2400 2400 3600 3600 3600
then these lists will give us a result value of each loop ran divided by the time it ran. so returned values 600 600 600 600 600 600 600 600 600
'''
#-------------------------------------------------------------Graph part

time2=time.time()
print("The program ran a total time of: " +str(datetime.timedelta(seconds=time2-time1)))  # tells us the total time of program ~1hour 50 minutes
X = ['1 Thread','2 Threads','4 Threads','8 Threads']
iops = [8327292,4379410,2276222,1178834]     #these are the final average values of the 1,2,4,8 threads of integer operations.
flops = [6839405,3747534,1996420,1045922]    #these are the final average values of the 1,2,4,8 threads of float operations.
gs=iops+flops
error = [160176, 102874,135532,66035,275148,183779, 86620,54234]
X_axis = np.arange(len(X))
bar1=plt.bar(X_axis - 0.2, iops, 0.4,yerr=error[:4], label = 'Iops',capsize=10)
bar2=plt.bar(X_axis + 0.2, flops, 0.4,yerr=error[4:], label = 'Flops',capsize=10)
for rect in bar1 + bar2:
    height = rect.get_height()
    plt.text(rect.get_x() + rect.get_width() / 1.0, height+3.0, f'{height:.0f}', ha='left', va='top')
plt.xticks(X_axis, X)
plt.xlabel("Number of Threads")
plt.ylabel("Number of operations")
plt.title("OPERATIONS PER SECOND GRAPH")
plt.legend()
plt.show()


