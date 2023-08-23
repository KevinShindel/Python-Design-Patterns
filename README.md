## Learning Python Design Patterns

### Chapter 1 [ MVC pattern ]
````text
TODO: Write description for MVC pattern
````
<img src="https://www.educative.io/api/page/5029697680310272/image/download/4900278303195136" alt='MVC' width="300" />

### Chapter 2 [ Singleton pattern ]
<img src="https://refactoring.guru/images/patterns/content/singleton/singleton-3x.png" alt="Singleton" width="300" />

````text
Singleton is a creational design pattern that lets you ensure that a class has only one instance, while providing a global access point to this instance.
All implementations of the Singleton have these two steps in common:

Make the default constructor private, to prevent other objects from using the new operator with the Singleton class.
Create a static creation method that acts as a constructor. Under the hood, this method calls the private constructor to create an object and saves it in a static field. All following calls to this method return the cached object.
If your code has access to the Singleton class, then it’s able to call the Singleton’s static method. So whenever that method is called, the same object is always returned.
````

### Chapter 3 [ Fabric pattern and Abstract Fabric pattern]
<img src="https://files.realpython.com/media/The-Factory-Method-Pattern-in-Python_Watermarked.6516a91d4d41.jpg" alt="Fabric" width="300" />

````text
Factory Method is a creational design pattern that provides an interface for creating objects in a superclass, but allows subclasses to alter the type of objects that will be created.
The Factory Method pattern suggests that you replace direct object construction calls (using the new operator) with calls to a special factory method. Don’t worry: the objects are still created via the new operator, but it’s being called from within the factory method. 
Objects returned by a factory method are often referred to as products.
````

### Chapter 4 [ Facade pattern ]

<img src="https://refactoring.guru/images/patterns/cards/facade-mini-3x.png" alt="facade pattern" width="300"/>

````text
Facade pattern used to decrease complexity and understand how system works
````

### Chapter 5 [ Proxy and Observer pattern ]
<img src="https://refactoring.guru/images/patterns/cards/proxy-mini-3x.png" width="300" alt="proxy" />
<img src="https://stackabuse.s3.amazonaws.com/media/observer-design-pattern-in-python-01.jpg" alt="observer" width="300"/>

### Chapter 6 [ Command pattern ]
<img src="https://www.tutorialspoint.com/python_design_patterns/images/architecture_of_command_pattern.jpg" alt="command" width="300">

````text
Command is a behavioral design pattern that turns a request into a stand-alone object that contains all 
information about the request. This transformation lets you pass requests as a method arguments, delay or 
queue a request’s execution, and support undoable operations.
````


### Chapter 7 [ Template pattern ]
<img src="https://refactoring.guru/images/patterns/diagrams/template-method/problem.png" alt="template" width="300" />

````text
Template Method is a behavioral design pattern that defines the skeleton of an algorithm in the superclass but lets subclasses override specific steps of the algorithm without changing its structure.
abstract steps must be implemented by every subclass
optional steps already have some default implementation, but still can be overridden if needed
````