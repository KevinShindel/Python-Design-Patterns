## Factory Pattern
<img src="https://refactoring.guru/images/patterns/content/factory-method/factory-method-en.png" width="300" alt="factory"/>

````text
Factory method is a creational design pattern which solves
 the problem of creating product objects without specifying their concrete classes.
````

````text
Usage examples: The Factory Method pattern is widely used in Python code. It’s very useful when you need to provide a high level of flexibility for your code.
Identification: Factory methods can be recognized by creation methods that construct objects from concrete classes. While concrete classes are used during the object creation, the return type of the factory methods is usually declared as either an abstract class or an interface.
````

## Prototype Pattern
<img src="https://refactoring.guru/images/patterns/cards/prototype-mini.png?id=bc3046bb39ff36574c08d49839fd1c8e" alt="prototype" width="200">

````text
Usage examples: The Prototype pattern is available in Python out of the box with a copy module.

Identification: The prototype can be easily recognized by a clone or copy methods, etc.
````

## Singleton Pattern
<img src="https://refactoring.guru/images/patterns/cards/singleton-mini.png?id=914e1565dfdf15f240e766163bd303ec" alt="singleton" width="200">

````text
Usage examples: A lot of developers consider the Singleton pattern an antipattern. That’s why its usage is on the decline in Python code.

Identification: Singleton can be recognized by a static creation method, which returns the same cached object.
````