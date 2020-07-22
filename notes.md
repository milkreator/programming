
##### notes  
  * glue components together  
  * **search for an approximate answer** using computer, not in math  
    - start from the problem, then split into smaller problems

#### The Elements of Programming  
  * 


#### Data Abstraction  
  * Data Abstraction Idea    

    Application Code (using Data)   
    ------ [ interface ] --------    
    Data Representatin (bits/bytes)    

  * changing the low-level data representation doesn't need to change the high-level code  


  * TODO  
    - class  


#### Adaptation  
  * adapt existing objects to look like other things  

  *  create your own abstractions that **mirror some aspect of your program** to work  
    - not only using those that are provided  
    - give you ownership of an abstraction   



#### Programming with objects  
  * Interfaces  

  * the most important is **the stack interface**, not the precise stack implementation  
    - class StackInterface(ABC)


  * notes  
    - A.__mro__ -> # object's method resolution order  (in Inheritance)  
     
    - dis.dis(f)  
      + check the machine instructions  

    -  
    - how does python work exactly?  the stackmachine  
      + form the basis of a simple virtual machine that executes an instruction sequence

  * inheritance  
    - extensibility -> many ways to do sth? many targets? 

       + interfaces  .  abstract base classes

    - sketchy.  implementation inheritance  
       + inherit from existing object to get functionality, then add new funcitonality  
       + inheriting from list, dict, etc... 
       + could get unintended behavior/side effects 

    - composition.  "is a " vs " has a" relationship  
       + car is an engine -> inheritance
       + car has an engine ->


    - Mixins -- modifier/behavior 
       + "Turbocharger on the engine" 

    - History on python  
       + current inheritance: "C3 linearization algorithm" 
       + 

  * TODO 
    - class  

#### State machines 
  *  how to design the soluton, and how to split the work into diff classes 
    - logic + control   
    - how to separate the functions  
    - how to test it 

  * Writing down lots of comments with thoughts/assumptions/details may be useful in this project.



####  Functional programming

#### Concurrency

#### Linguistic abstraction  

#### reference
